"""
CLINK — Doctor Service
Handles doctor dashboard operations and case management.
"""
from app.extensions import db
from app.models.symptom_record import SymptomRecord
from app.models.patient import Patient
from app.models.appointment import Appointment
from app.services.notification_service import NotificationService


class DoctorService:
    """Business logic for doctor operations."""

    @staticmethod
    def get_assigned_cases(doctor_id):
        """
        UC009: Get all assigned patient cases, sorted by urgency.
        Urgent cases appear first. Among cases with the same urgency,
        older patients (earlier date of birth) are prioritised.
        """
        records = SymptomRecord.query.join(Patient, SymptomRecord.patient_id == Patient.id)\
            .filter(SymptomRecord.doctor_id == doctor_id)\
            .order_by(
                db.case(
                    (SymptomRecord.urgency_level == 'urgent', 0),
                    else_=1
                ),
                db.func.coalesce(Patient.dob, db.func.current_date()).asc(),
                SymptomRecord.created_at.desc()
            ).all()
        return records

    @staticmethod
    def get_case_details(record_id, doctor_id):
        """UC010b: Get detailed case information including AI triage results."""
        record = SymptomRecord.query.filter_by(
            id=record_id,
            doctor_id=doctor_id
        ).first()
        return record

    @staticmethod
    def update_case_status(record_id, doctor_id, status, notes=None):
        """
        UC010: Update case status and consultation notes.
        """
        record = SymptomRecord.query.filter_by(
            id=record_id,
            doctor_id=doctor_id
        ).first()

        if not record:
            return None, 'Case not found or not assigned to you.'

        valid_statuses = ['new', 'in-review', 'consulted', 'closed']
        if status not in valid_statuses:
            return None, f'Invalid status. Must be one of: {", ".join(valid_statuses)}'

        record.case_status = status
        if notes:
            record.consultation_notes = notes

        db.session.commit()

        # Notify patient
        NotificationService.create_notification(
            user_id=record.patient_id,
            user_role='patient',
            message=f'Your case status has been updated to: {status}.',
            notification_type='case_update'
        )

        return record, None

    @staticmethod
    def get_dashboard_stats(doctor_id):
        """Get statistics for doctor dashboard."""
        total = SymptomRecord.query.filter_by(doctor_id=doctor_id).count()
        urgent = SymptomRecord.query.filter_by(doctor_id=doctor_id, urgency_level='urgent').count()
        new_cases = SymptomRecord.query.filter_by(doctor_id=doctor_id, case_status='new').count()
        in_review = SymptomRecord.query.filter_by(doctor_id=doctor_id, case_status='in-review').count()

        appointments_today = Appointment.query.filter_by(doctor_id=doctor_id)\
            .filter(Appointment.date == db.func.current_date())\
            .filter(Appointment.status.in_(['scheduled'])).count()

        return {
            'totalCases': total,
            'urgentCases': urgent,
            'newCases': new_cases,
            'inReview': in_review,
            'appointmentsToday': appointments_today,
        }
