"""
CLINK — Appointment Controller
Handles appointment slot retrieval and booking.
"""
from flask import Blueprint, request, jsonify, url_for
from flask_login import login_required, current_user
from app.controllers.auth_controller import role_required
from app.services.appointment_service import AppointmentService

appointment_bp = Blueprint('appointment', __name__)


@appointment_bp.route('/api/appointment/slots', methods=['GET'])
@role_required('patient')
def get_slots():
    """Get available appointment slots for a doctor."""
    doctor_id = request.args.get('doctor_id', type=int)
    urgency = request.args.get('urgency', 'non-urgent')

    if not doctor_id:
        return jsonify({'success': False, 'error': 'Doctor ID is required.'}), 400

    slots = AppointmentService.get_available_slots(doctor_id, urgency)
    return jsonify({'success': True, 'slots': slots})


@appointment_bp.route('/api/appointment/book', methods=['POST'])
@role_required('patient')
def book_appointment():
    """UC007: Book an appointment."""
    data = request.get_json()
    if not data:
        return jsonify({'success': False, 'error': 'Invalid request data.'}), 400

    appointment, error = AppointmentService.book_appointment(
        patient_id=current_user.id,
        doctor_id=data.get('doctorId'),
        record_id=data.get('recordId'),
        appt_date=data.get('date'),
        appt_time=data.get('time'),
    )

    if error:
        return jsonify({'success': False, 'error': error}), 400

    return jsonify({
        'success': True,
        'message': 'Appointment booked successfully!',
        'appointment': appointment.to_dict()
    })


@appointment_bp.route('/api/appointment/<int:appt_id>', methods=['GET'])
@login_required
def get_appointment(appt_id):
    """Get appointment details."""
    from app.models.appointment import Appointment
    appointment = Appointment.query.get(appt_id)
    if not appointment:
        return jsonify({'success': False, 'error': 'Appointment not found.'}), 404
    return jsonify({'success': True, 'appointment': appointment.to_dict()})


@appointment_bp.route('/api/appointment/<int:appt_id>/status', methods=['PUT'])
@role_required('doctor', 'admin')
def update_appointment_status(appt_id):
    """Update appointment status."""
    data = request.get_json()
    new_status = data.get('status', '')

    appointment, error = AppointmentService.update_status(appt_id, new_status)
    if error:
        return jsonify({'success': False, 'error': error}), 400

    return jsonify({
        'success': True,
        'message': f'Appointment status updated to {new_status}.',
        'appointment': appointment.to_dict()
    })


@appointment_bp.route('/api/appointment/patient', methods=['GET'])
@role_required('patient')
def get_patient_appointments():
    """Get all appointments for the current patient."""
    appointments = AppointmentService.get_patient_appointments(current_user.id)
    return jsonify({
        'success': True,
        'appointments': [a.to_dict() for a in appointments]
    })
