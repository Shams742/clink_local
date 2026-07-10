"""
CLINK — Appointment Service
Handles appointment scheduling, slot generation, and booking.
"""
from datetime import datetime, timedelta, date, time
from app.extensions import db
from app.models.appointment import Appointment
from app.models.doctor import Doctor
from app.models.symptom_record import SymptomRecord
from app.services.notification_service import NotificationService


class AppointmentService:
    """Business logic for appointment operations."""

    # Clinic hours
    SLOT_START_HOUR = 8   # 8:00 AM
    SLOT_END_HOUR = 17    # 5:00 PM
    SLOT_DURATION = 30    # minutes

    @classmethod
    def get_available_slots(cls, doctor_id, urgency_level='non-urgent', days_ahead=7):
        """
        Generate available appointment slots for a doctor.
        Urgent patients see slots starting from today/tomorrow;
        non-urgent start from a few days later.
        Uses doctor's custom schedule_hours if configured.
        """
        import json

        doctor = Doctor.query.get(doctor_id)
        if not doctor:
            return []

        # Use doctor-specific schedule hours if available, else defaults
        slot_start = cls.SLOT_START_HOUR
        slot_end = cls.SLOT_END_HOUR
        if hasattr(doctor, 'schedule_hours') and doctor.schedule_hours:
            try:
                hours = json.loads(doctor.schedule_hours)
                slot_start = int(hours.get('start', cls.SLOT_START_HOUR))
                slot_end = int(hours.get('end', cls.SLOT_END_HOUR))
            except (json.JSONDecodeError, ValueError, TypeError):
                pass  # Fall back to defaults

        # Urgent: start from tomorrow; Non-urgent: start from 3 days out
        if urgency_level == 'urgent':
            start_date = date.today() + timedelta(days=1)
        else:
            start_date = date.today() + timedelta(days=3)

        end_date = start_date + timedelta(days=days_ahead)

        # Get existing appointments for this doctor in the date range
        existing = Appointment.query.filter(
            Appointment.doctor_id == doctor_id,
            Appointment.date >= start_date,
            Appointment.date <= end_date,
            Appointment.status.in_(['requested', 'scheduled'])
        ).all()

        booked_slots = {(a.date, a.time) for a in existing}

        slots = []
        current_date = start_date
        while current_date <= end_date:
            # Allow booking 7 days a week
            hour = slot_start
            minute = 0
            while hour < slot_end:
                slot_time = time(hour, minute)
                if (current_date, slot_time) not in booked_slots:
                    slots.append({
                        'date': current_date.isoformat(),
                        'time': slot_time.strftime('%H:%M'),
                        'displayDate': current_date.strftime('%A, %B %d, %Y'),
                        'displayTime': slot_time.strftime('%I:%M %p'),
                    })
                minute += cls.SLOT_DURATION
                if minute >= 60:
                    hour += 1
                    minute = 0
            current_date += timedelta(days=1)

        return slots

    @classmethod
    def book_appointment(cls, patient_id, doctor_id, record_id, appt_date, appt_time):
        """
        UC007: Book an appointment.
        """
        # Parse date and time
        try:
            if isinstance(appt_date, str):
                appt_date = date.fromisoformat(appt_date)
            if isinstance(appt_time, str):
                parts = appt_time.split(':')
                appt_time = time(int(parts[0]), int(parts[1]))
        except (ValueError, IndexError):
            return None, 'Invalid date or time format.'

        # Check if slot is still available (conflict detection)
        existing = Appointment.query.filter_by(
            doctor_id=doctor_id,
            date=appt_date,
            time=appt_time,
        ).filter(Appointment.status.in_(['requested', 'scheduled'])).first()

        if existing:
            return None, 'This slot is no longer available. Please select another.'

        appointment = Appointment(
            patient_id=patient_id,
            doctor_id=doctor_id,
            record_id=record_id,
            date=appt_date,
            time=appt_time,
            status='scheduled'
        )
        db.session.add(appointment)

        # Update symptom record case status
        if record_id:
            record = SymptomRecord.query.get(record_id)
            if record:
                record.case_status = 'in-review'

        db.session.commit()

        # UC008: Trigger notification
        doctor = Doctor.query.get(doctor_id)
        NotificationService.create_notification(
            user_id=patient_id,
            user_role='patient',
            message=f'Your appointment with Dr. {doctor.name} has been scheduled for {appt_date.strftime("%B %d, %Y")} at {appt_time.strftime("%I:%M %p")}.',
            notification_type='appointment_confirmed'
        )
        NotificationService.create_notification(
            user_id=doctor_id,
            user_role='doctor',
            message=f'New appointment scheduled on {appt_date.strftime("%B %d, %Y")} at {appt_time.strftime("%I:%M %p")}.',
            notification_type='appointment_confirmed'
        )

        return appointment, None

    @staticmethod
    def get_patient_appointments(patient_id):
        """Get all appointments for a patient."""
        return Appointment.query.filter_by(patient_id=patient_id)\
            .order_by(Appointment.date.desc(), Appointment.time.desc()).all()

    @staticmethod
    def get_doctor_appointments(doctor_id):
        """Get all appointments for a doctor."""
        return Appointment.query.filter_by(doctor_id=doctor_id)\
            .order_by(Appointment.date.asc(), Appointment.time.asc()).all()

    @staticmethod
    def update_status(appointment_id, new_status, user_role=None):
        """Update appointment status."""
        appointment = Appointment.query.get(appointment_id)
        if not appointment:
            return None, 'Appointment not found.'

        valid_statuses = ['requested', 'scheduled', 'completed', 'cancelled']
        if new_status not in valid_statuses:
            return None, f'Invalid status. Must be one of: {", ".join(valid_statuses)}'

        old_status = appointment.status
        appointment.status = new_status
        db.session.commit()

        # Notify patient of status change
        NotificationService.create_notification(
            user_id=appointment.patient_id,
            user_role='patient',
            message=f'Your appointment on {appointment.date.strftime("%B %d, %Y")} has been updated to: {new_status}.',
            notification_type='appointment_updated'
        )

        return appointment, None
