"""
CLINK — Doctor Controller
Handles doctor dashboard, case management, and notifications.
"""
from flask import Blueprint, request, jsonify, render_template
from flask_login import login_required, current_user
from app.controllers.auth_controller import role_required
from app.services.doctor_service import DoctorService
from app.services.appointment_service import AppointmentService
from app.services.notification_service import NotificationService

doctor_bp = Blueprint('doctor', __name__)


# --- Page Routes ---

@doctor_bp.route('/doctor/dashboard')
@role_required('doctor')
def dashboard():
    cases = DoctorService.get_assigned_cases(current_user.id)
    stats = DoctorService.get_dashboard_stats(current_user.id)
    appointments = AppointmentService.get_doctor_appointments(current_user.id)
    unread = NotificationService.get_unread_count(current_user.id, 'doctor')
    return render_template('doctor/dashboard.html',
                           cases=cases,
                           stats=stats,
                           appointments=appointments,
                           unread_count=unread)


@doctor_bp.route('/doctor/appointments')
@role_required('doctor')
def appointments_page():
    status_filter = request.args.get('status', 'all')
    from app.models.appointment import Appointment
    query = Appointment.query.filter_by(doctor_id=current_user.id)
    if status_filter in ['scheduled', 'completed', 'cancelled', 'requested']:
        query = query.filter_by(status=status_filter)
    appointments = query.order_by(Appointment.date.asc(), Appointment.time.asc()).all()
    return render_template('doctor/appointments.html', appointments=appointments, status_filter=status_filter)


@doctor_bp.route('/doctor/case/<int:record_id>')
@role_required('doctor')
def case_details(record_id):
    record = DoctorService.get_case_details(record_id, current_user.id)
    if not record:
        return render_template('errors/404.html'), 404
    return render_template('doctor/case_details.html', record=record)


# --- API Routes ---

@doctor_bp.route('/api/doctor/cases', methods=['GET'])
@role_required('doctor')
def get_cases():
    """UC009: Get prioritised case list."""
    cases = DoctorService.get_assigned_cases(current_user.id)
    return jsonify({
        'success': True,
        'cases': [c.to_dict() for c in cases]
    })


@doctor_bp.route('/api/doctor/cases/<int:record_id>', methods=['GET'])
@role_required('doctor')
def get_case(record_id):
    """UC010b: Get case details with AI triage results."""
    record = DoctorService.get_case_details(record_id, current_user.id)
    if not record:
        return jsonify({'success': False, 'error': 'Case not found.'}), 404
    return jsonify({'success': True, 'case': record.to_dict()})


@doctor_bp.route('/api/doctor/cases/<int:record_id>/status', methods=['PUT'])
@role_required('doctor')
def update_case(record_id):
    """UC010: Update case status."""
    data = request.get_json()
    if not data:
        return jsonify({'success': False, 'error': 'Invalid request data.'}), 400

    record, error = DoctorService.update_case_status(
        record_id=record_id,
        doctor_id=current_user.id,
        status=data.get('status', ''),
        notes=data.get('notes')
    )

    if error:
        return jsonify({'success': False, 'error': error}), 400

    return jsonify({
        'success': True,
        'message': 'Case status updated successfully.',
        'case': record.to_dict()
    })


@doctor_bp.route('/api/doctor/cases/<int:record_id>/notes', methods=['PUT'])
@role_required('doctor')
def save_case_notes(record_id):
    """Save consultation notes independently without changing case status."""
    data = request.get_json()
    if not data:
        return jsonify({'success': False, 'error': 'Invalid request data.'}), 400

    record = DoctorService.get_case_details(record_id, current_user.id)
    if not record:
        return jsonify({'success': False, 'error': 'Case not found or not assigned to you.'}), 404

    from app.extensions import db
    record.consultation_notes = data.get('notes', record.consultation_notes)
    db.session.commit()

    return jsonify({
        'success': True,
        'message': 'Consultation notes saved successfully.',
        'case': record.to_dict()
    })


@doctor_bp.route('/api/doctor/stats', methods=['GET'])
@role_required('doctor')
def get_stats():
    stats = DoctorService.get_dashboard_stats(current_user.id)
    return jsonify({'success': True, 'stats': stats})


@doctor_bp.route('/api/doctor/notifications', methods=['GET'])
@role_required('doctor')
def get_notifications():
    notifications = NotificationService.get_user_notifications(current_user.id, 'doctor')
    unread = NotificationService.get_unread_count(current_user.id, 'doctor')
    return jsonify({
        'success': True,
        'notifications': [n.to_dict() for n in notifications],
        'unreadCount': unread
    })


@doctor_bp.route('/api/doctor/notifications/<int:notif_id>/read', methods=['PUT'])
@role_required('doctor')
def mark_notification_read(notif_id):
    notification, error = NotificationService.mark_as_read(notif_id, current_user.id, 'doctor')
    if error:
        return jsonify({'success': False, 'error': error}), 404
    return jsonify({'success': True})
