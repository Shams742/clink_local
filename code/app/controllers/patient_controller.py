"""
CLINK — Patient Controller
Handles patient dashboard, symptom submission, triage view, and notifications.
"""
from flask import Blueprint, request, jsonify, render_template
from flask_login import login_required, current_user
from app.controllers.auth_controller import role_required
from app.services.patient_service import PatientService
from app.services.ai_triage_service import AITriageService
from app.services.notification_service import NotificationService
from app.services.appointment_service import AppointmentService

patient_bp = Blueprint('patient', __name__)


# --- Page Routes ---

@patient_bp.route('/patient/dashboard')
@role_required('patient')
def dashboard():
    records = PatientService.get_patient_records(current_user.id)
    appointments = AppointmentService.get_patient_appointments(current_user.id)
    unread = NotificationService.get_unread_count(current_user.id, 'patient')
    return render_template('patient/dashboard.html',
                           records=records,
                           appointments=appointments,
                           unread_count=unread)


@patient_bp.route('/patient/submit-symptoms')
@role_required('patient')
def submit_symptoms_page():
    symptoms = AITriageService.get_symptom_list()
    symptom_codes = AITriageService.get_symptom_codes()
    return render_template('patient/submit_symptoms.html',
                           symptoms=symptoms,
                           symptom_codes=symptom_codes)


@patient_bp.route('/patient/triage/<int:record_id>')
@role_required('patient')
def triage_result_page(record_id):
    record = PatientService.get_record(record_id, current_user.id)
    if not record:
        return render_template('errors/404.html'), 404
    return render_template('patient/triage_result.html', record=record)


@patient_bp.route('/patient/book-appointment/<int:record_id>')
@role_required('patient')
def book_appointment_page(record_id):
    record = PatientService.get_record(record_id, current_user.id)
    if not record:
        return render_template('errors/404.html'), 404
    return render_template('patient/book_appointment.html', record=record)


@patient_bp.route('/patient/notifications')
@role_required('patient')
def notifications_page():
    notifications = NotificationService.get_user_notifications(current_user.id, 'patient')
    return render_template('patient/notifications.html', notifications=notifications)


@patient_bp.route('/patient/profile')
@role_required('patient')
def profile_page():
    return render_template('patient/profile.html')


@patient_bp.route('/patient/history')
@role_required('patient')
def history_page():
    from app.models.symptom_record import SymptomRecord
    
    urgency = request.args.get('urgency', 'all')
    sort_order = request.args.get('sort', 'desc')
    
    query = SymptomRecord.query.filter_by(patient_id=current_user.id)
    
    if urgency in ['urgent', 'non-urgent']:
        query = query.filter_by(urgency_level=urgency)
        
    if sort_order == 'asc':
        query = query.order_by(SymptomRecord.created_at.asc())
    else:
        query = query.order_by(SymptomRecord.created_at.desc())
        
    records = query.all()
    return render_template('patient/history.html', records=records, urgency=urgency, sort=sort_order)




# --- API Routes ---

@patient_bp.route('/api/patient/symptoms', methods=['POST'])
@role_required('patient')
def submit_symptoms():
    """UC002: Submit symptoms for AI analysis."""
    data = request.get_json()
    if not data:
        return jsonify({'success': False, 'error': 'Invalid request data.'}), 400

    symptoms_list = data.get('symptoms', [])
    symptom_details = data.get('details', '')

    if not symptoms_list:
        return jsonify({'success': False, 'error': 'Please select at least one symptom.'}), 400

    record, error = PatientService.submit_symptoms(
        patient_id=current_user.id,
        symptom_details=symptom_details,
        symptoms_list=symptoms_list
    )

    if error:
        return jsonify({'success': False, 'error': error}), 500

    return jsonify({
        'success': True,
        'message': 'Symptoms submitted and analysed successfully!',
        'record': record.to_dict(),
        'recordId': record.id
    })


@patient_bp.route('/api/patient/triage/<int:record_id>', methods=['GET'])
@role_required('patient')
def get_triage_result(record_id):
    """UC006: View triage result."""
    record = PatientService.get_record(record_id, current_user.id)
    if not record:
        return jsonify({'success': False, 'error': 'Record not found.'}), 404
    return jsonify({'success': True, 'record': record.to_dict()})


@patient_bp.route('/api/patient/records', methods=['GET'])
@role_required('patient')
def get_records():
    """Get all patient records."""
    records = PatientService.get_patient_records(current_user.id)
    return jsonify({
        'success': True,
        'records': [r.to_dict() for r in records]
    })


@patient_bp.route('/api/patient/notifications', methods=['GET'])
@role_required('patient')
def get_notifications():
    notifications = NotificationService.get_user_notifications(current_user.id, 'patient')
    unread = NotificationService.get_unread_count(current_user.id, 'patient')
    return jsonify({
        'success': True,
        'notifications': [n.to_dict() for n in notifications],
        'unreadCount': unread
    })


@patient_bp.route('/api/patient/notifications/<int:notif_id>/read', methods=['PUT'])
@role_required('patient')
def mark_notification_read(notif_id):
    notification, error = NotificationService.mark_as_read(notif_id, current_user.id, 'patient')
    if error:
        return jsonify({'success': False, 'error': error}), 404
    return jsonify({'success': True})


@patient_bp.route('/api/patient/notifications/read-all', methods=['PUT'])
@role_required('patient')
def mark_all_read():
    NotificationService.mark_all_read(current_user.id, 'patient')
    return jsonify({'success': True})


@patient_bp.route('/api/patient/profile', methods=['GET'])
@role_required('patient')
def get_patient_profile():
    return jsonify({
        'success': True,
        'patient': current_user.to_dict()
    })


@patient_bp.route('/api/patient/profile', methods=['PUT'])
@role_required('patient')
def update_patient_profile():
    data = request.get_json()
    if not data:
        return jsonify({'success': False, 'error': 'Invalid request data.'}), 400
        
    current_password = data.get('current_password', '')
    if not current_password:
        return jsonify({'success': False, 'error': 'Current password is required to save changes.'}), 400
        
    from app.services.auth_service import AuthService
    if not AuthService.check_password(current_password, current_user.password):
        return jsonify({'success': False, 'error': 'Incorrect current password.'}), 400
        
    name = data.get('name', '').strip()
    phone = data.get('phone', '').strip()
    gender = data.get('gender', '').strip()
    dob = data.get('dob', '').strip()
    new_password = data.get('new_password', '').strip()
    
    if name:
        valid, err = AuthService.validate_name(name)
        if not valid:
            return jsonify({'success': False, 'error': err}), 400
        current_user.name = name
        
    if phone:
        valid, err = AuthService.validate_phone(phone)
        if not valid:
            return jsonify({'success': False, 'error': err}), 400
        current_user.phone = phone

    if gender:
        valid, err = AuthService.validate_gender(gender)
        if not valid:
            return jsonify({'success': False, 'error': err}), 400
        current_user.gender = gender

    if dob:
        valid, err = AuthService.validate_dob(dob)
        if not valid:
            return jsonify({'success': False, 'error': err}), 400
        from datetime import datetime as dt
        current_user.dob = dt.strptime(dob, '%Y-%m-%d').date()

    if new_password:
        valid, err = AuthService.validate_password(new_password)
        if not valid:
            return jsonify({'success': False, 'error': err}), 400
        current_user.password = AuthService.hash_password(new_password)
        
    from app.extensions import db
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': 'Profile updated successfully!',
        'patient': current_user.to_dict()
    })


@patient_bp.route('/api/patient/appointments/<int:appt_id>/cancel', methods=['PUT'])
@role_required('patient')
def cancel_patient_appointment(appt_id):
    from app.models.appointment import Appointment
    from app.services.notification_service import NotificationService
    
    appointment = Appointment.query.get(appt_id)
    if not appointment:
        return jsonify({'success': False, 'error': 'Appointment not found.'}), 404
        
    if appointment.patient_id != current_user.id:
        return jsonify({'success': False, 'error': 'You do not have permission to cancel this appointment.'}), 403
        
    if appointment.status not in ['requested', 'scheduled']:
        return jsonify({'success': False, 'error': f'Cannot cancel appointment with status: {appointment.status}.'}), 400
        
    appointment.status = 'cancelled'
    
    # Notify doctor
    NotificationService.create_notification(
        user_id=appointment.doctor_id,
        user_role='doctor',
        message=f'Appointment on {appointment.date.strftime("%B %d, %Y")} at {appointment.time.strftime("%I:%M %p")} has been cancelled by patient {current_user.name}.',
        notification_type='appointment_updated'
    )
    
    # Notify patient
    NotificationService.create_notification(
        user_id=appointment.patient_id,
        user_role='patient',
        message=f'You have cancelled your appointment on {appointment.date.strftime("%B %d, %Y")} at {appointment.time.strftime("%I:%M %p")}.',
        notification_type='appointment_updated'
    )
    
    from app.extensions import db
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': 'Appointment cancelled successfully.'
    })


