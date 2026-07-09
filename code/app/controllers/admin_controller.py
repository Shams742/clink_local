"""
CLINK — Admin Controller
Handles admin dashboard, user management, and schedule configuration.
"""
from flask import Blueprint, request, jsonify, render_template
from flask_login import login_required, current_user
from app.controllers.auth_controller import role_required
from app.services.admin_service import AdminService
from app.models.notification import Notification
from app.models.appointment import Appointment
from app.models.symptom_record import SymptomRecord
from app.models.patient import Patient
from app.models.doctor import Doctor

admin_bp = Blueprint('admin', __name__)


# --- Page Routes ---

@admin_bp.route('/admin/dashboard')
@role_required('admin')
def dashboard():
    stats = AdminService.get_dashboard_stats()
    patients = AdminService.get_all_patients()
    doctors = AdminService.get_all_doctors()
    return render_template('admin/dashboard.html',
                           stats=stats,
                           patients=patients,
                           doctors=doctors)


@admin_bp.route('/admin/manage-users')
@role_required('admin')
def manage_users():
    patients = AdminService.get_all_patients()
    doctors = AdminService.get_all_doctors()
    return render_template('admin/manage_users.html',
                           patients=patients,
                           doctors=doctors)


@admin_bp.route('/admin/schedules')
@role_required('admin')
def configure_schedules():
    doctors = AdminService.get_all_doctors()
    return render_template('admin/configure_schedules.html', doctors=doctors)


@admin_bp.route('/admin/notifications')
@role_required('admin')
def notifications_page():
    page = request.args.get('page', 1, type=int)
    role_filter = request.args.get('role', 'all')
    query = Notification.query
    if role_filter != 'all':
        query = query.filter_by(user_role=role_filter)
    pagination = query.order_by(Notification.timestamp.desc()).paginate(page=page, per_page=20, error_out=False)
    return render_template('admin/notifications.html',
                           notifications=pagination.items,
                           pagination=pagination,
                           role_filter=role_filter)


@admin_bp.route('/admin/reports')
@role_required('admin')
def reports_page():
    stats = AdminService.get_dashboard_stats()
    chart_data = AdminService.get_reports_data()
    model_accuracy = AdminService.get_model_accuracy()
    model_robustness = AdminService.get_model_robustness()
    return render_template('admin/reports.html', stats=stats, chart_data=chart_data,
                           model_accuracy=model_accuracy, model_robustness=model_robustness)


@admin_bp.route('/admin/audit-log')
@role_required('admin')
def audit_log_page():
    page = request.args.get('page', 1, type=int)
    pagination = AdminService.get_audit_log(page=page, per_page=25)
    return render_template('admin/audit_log.html', entries=pagination.items, pagination=pagination)


# --- API Routes ---

@admin_bp.route('/api/admin/stats', methods=['GET'])
@role_required('admin')
def get_stats():
    stats = AdminService.get_dashboard_stats()
    return jsonify({'success': True, 'stats': stats})


@admin_bp.route('/api/admin/reports', methods=['GET'])
@role_required('admin')
def get_reports_api():
    chart_data = AdminService.get_reports_data()
    return jsonify({'success': True, 'data': chart_data})


@admin_bp.route('/admin/email-log')
@role_required('admin')
def email_log_page():
    from app.services.notification_service import EMAIL_LOG
    emails = list(reversed(EMAIL_LOG))  # newest first
    return render_template('admin/email_log.html', emails=emails)


@admin_bp.route('/api/admin/email-log', methods=['GET'])
@role_required('admin')
def get_email_log_api():
    from app.services.notification_service import EMAIL_LOG
    return jsonify({'success': True, 'emails': list(reversed(EMAIL_LOG)), 'total': len(EMAIL_LOG)})


@admin_bp.route('/api/admin/notifications/<int:notif_id>/read', methods=['PUT'])
@role_required('admin')
def mark_notification_read(notif_id):
    notif = Notification.query.get(notif_id)
    if not notif:
        return jsonify({'success': False, 'error': 'Notification not found.'}), 404
    from app.extensions import db
    notif.is_read = True
    db.session.commit()
    return jsonify({'success': True, 'message': 'Marked as read.'})


@admin_bp.route('/api/admin/users', methods=['GET'])
@role_required('admin')
def get_users():
    """UC011: List all users."""
    role_filter = request.args.get('role', 'all')
    result = {}
    if role_filter in ('all', 'patient'):
        result['patients'] = [p.to_dict() for p in AdminService.get_all_patients()]
    if role_filter in ('all', 'doctor'):
        result['doctors'] = [d.to_dict() for d in AdminService.get_all_doctors()]
    return jsonify({'success': True, **result})


@admin_bp.route('/api/admin/users/doctor', methods=['POST'])
@role_required('admin')
def create_doctor():
    """UC011: Create a new doctor."""
    data = request.get_json()
    if not data:
        return jsonify({'success': False, 'error': 'Invalid request data.'}), 400

    doctor, error = AdminService.create_doctor(
        name=data.get('name', ''),
        email=data.get('email', ''),
        password=data.get('password', ''),
        specialization=data.get('specialization', ''),
    )

    if error:
        return jsonify({'success': False, 'error': error}), 400

    AdminService.log_action(current_user.id, 'create_doctor', 'doctor', doctor.id, f'Created Dr. {doctor.name}')

    return jsonify({
        'success': True,
        'message': 'Doctor account created successfully!',
        'doctor': doctor.to_dict()
    })


@admin_bp.route('/api/admin/users/<int:user_id>', methods=['PUT'])
@role_required('admin')
def update_user(user_id):
    """UC011: Update user."""
    data = request.get_json()
    role = data.get('role', '')

    update_fields = {}
    for field in ['name', 'email', 'specialization', 'availability', 'phone']:
        if field in data:
            update_fields[field] = data[field]

    user, error = AdminService.update_user(user_id, role, **update_fields)
    if error:
        return jsonify({'success': False, 'error': error}), 400

    AdminService.log_action(current_user.id, 'update_user', role, user_id, f'Updated {role} #{user_id}')

    return jsonify({
        'success': True,
        'message': 'User updated successfully.',
        'user': user.to_dict()
    })


@admin_bp.route('/api/admin/users/<int:user_id>/deactivate', methods=['PUT'])
@role_required('admin')
def deactivate_user(user_id):
    """UC011: Deactivate user."""
    data = request.get_json()
    role = data.get('role', '')

    user, error = AdminService.deactivate_user(user_id, role)
    if error:
        return jsonify({'success': False, 'error': error}), 400

    AdminService.log_action(current_user.id, 'deactivate_user', role, user_id, f'Deactivated {role} #{user_id}')

    return jsonify({'success': True, 'message': 'User deactivated.'})


@admin_bp.route('/api/admin/users/<int:user_id>/activate', methods=['PUT'])
@role_required('admin')
def activate_user(user_id):
    """UC011: Activate user."""
    data = request.get_json()
    role = data.get('role', '')

    user, error = AdminService.activate_user(user_id, role)
    if error:
        return jsonify({'success': False, 'error': error}), 400

    AdminService.log_action(current_user.id, 'activate_user', role, user_id, f'Activated {role} #{user_id}')

    return jsonify({'success': True, 'message': 'User activated.'})


@admin_bp.route('/api/admin/schedules/<int:doctor_id>', methods=['PUT'])
@role_required('admin')
def update_schedule(doctor_id):
    """UC012: Update doctor availability."""
    data = request.get_json()
    availability = data.get('availability', '')

    doctor, error = AdminService.update_doctor_availability(doctor_id, availability)
    if error:
        return jsonify({'success': False, 'error': error}), 400

    AdminService.log_action(current_user.id, 'update_availability', 'doctor', doctor_id, f'Set {doctor.name} to {availability}')

    return jsonify({
        'success': True,
        'message': f'Dr. {doctor.name} availability updated to {availability}.',
        'doctor': doctor.to_dict()
    })


@admin_bp.route('/api/admin/schedules/<int:doctor_id>/hours', methods=['PUT'])
@role_required('admin')
def update_schedule_hours(doctor_id):
    """Update doctor working hours (start/end in 24h format)."""
    data = request.get_json()
    start_hour = data.get('start')
    end_hour = data.get('end')

    if start_hour is None or end_hour is None:
        return jsonify({'success': False, 'error': 'start and end hours required.'}), 400

    try:
        start_hour = int(start_hour)
        end_hour = int(end_hour)
        if not (0 <= start_hour < end_hour <= 23):
            raise ValueError
    except (ValueError, TypeError):
        return jsonify({'success': False, 'error': 'Invalid hours. start must be < end, both 0-23.'}), 400

    doctor = Doctor.query.get(doctor_id)
    if not doctor:
        return jsonify({'success': False, 'error': 'Doctor not found.'}), 404

    import json
    from app.extensions import db
    doctor.schedule_hours = json.dumps({'start': start_hour, 'end': end_hour})
    db.session.commit()

    return jsonify({
        'success': True,
        'message': f'Dr. {doctor.name} schedule updated to {start_hour:02d}:00 – {end_hour:02d}:00.',
        'doctor': doctor.to_dict()
    })
