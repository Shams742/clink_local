"""
CLINK — Admin Service
Handles user management and schedule configuration.
"""
from app.extensions import db
from app.models.patient import Patient
from app.models.doctor import Doctor
from app.models.admin import Admin
from app.models.appointment import Appointment
from app.models.symptom_record import SymptomRecord
from app.services.auth_service import AuthService


class AdminService:
    """Business logic for administrative operations."""

    # --- User Management (UC011) ---

    @staticmethod
    def get_all_patients():
        return Patient.query.order_by(Patient.created_at.desc()).all()

    @staticmethod
    def get_all_doctors():
        return Doctor.query.order_by(Doctor.name.asc()).all()

    @staticmethod
    def create_doctor(name, email, password, specialization):
        """Create a new doctor account."""
        valid, err = AuthService.validate_name(name)
        if not valid:
            return None, err
        valid, err = AuthService.validate_email(email)
        if not valid:
            return None, err
        valid, err = AuthService.validate_password(password)
        if not valid:
            return None, err

        if Doctor.query.filter_by(email=email).first():
            return None, 'A doctor with this email already exists.'
        if Patient.query.filter_by(email=email).first():
            return None, 'An account with this email already exists.'

        doctor = Doctor(
            name=name.strip(),
            email=email.strip().lower(),
            password=AuthService.hash_password(password),
            specialization=specialization,
        )
        db.session.add(doctor)
        db.session.commit()
        return doctor, None

    @staticmethod
    def update_user(user_id, role, **kwargs):
        """Update a user's information."""
        if role == 'patient':
            user = Patient.query.get(user_id)
        elif role == 'doctor':
            user = Doctor.query.get(user_id)
        else:
            return None, 'Invalid role.'

        if not user:
            return None, 'User not found.'

        for key, value in kwargs.items():
            if hasattr(user, key) and value is not None:
                setattr(user, key, value)

        db.session.commit()
        return user, None

    @staticmethod
    def deactivate_user(user_id, role):
        """Deactivate a user account."""
        if role == 'patient':
            user = Patient.query.get(user_id)
        elif role == 'doctor':
            user = Doctor.query.get(user_id)
        else:
            return None, 'Invalid role.'

        if not user:
            return None, 'User not found.'

        user.account_status = 'inactive'
        db.session.commit()
        return user, None

    @staticmethod
    def activate_user(user_id, role):
        """Reactivate a user account."""
        if role == 'patient':
            user = Patient.query.get(user_id)
        elif role == 'doctor':
            user = Doctor.query.get(user_id)
        else:
            return None, 'Invalid role.'

        if not user:
            return None, 'User not found.'

        user.account_status = 'active'
        db.session.commit()
        return user, None

    # --- Schedule Configuration (UC012) ---

    @staticmethod
    def update_doctor_availability(doctor_id, availability):
        """Update doctor availability status."""
        doctor = Doctor.query.get(doctor_id)
        if not doctor:
            return None, 'Doctor not found.'

        valid_states = ['available', 'unavailable']
        if availability not in valid_states:
            return None, f'Invalid availability. Must be one of: {", ".join(valid_states)}'

        doctor.availability = availability
        db.session.commit()
        return doctor, None

    @staticmethod
    def get_dashboard_stats():
        """Get admin dashboard statistics."""
        return {
            'totalPatients': Patient.query.count(),
            'totalDoctors': Doctor.query.count(),
            'activePatients': Patient.query.filter_by(account_status='active').count(),
            'activeDoctors': Doctor.query.filter_by(account_status='active').count(),
            'totalAppointments': Appointment.query.count(),
            'scheduledAppointments': Appointment.query.filter_by(status='scheduled').count(),
            'totalRecords': SymptomRecord.query.count(),
            'urgentCases': SymptomRecord.query.filter_by(urgency_level='urgent').count(),
        }

    @staticmethod
    def get_reports_data():
        """Get aggregated data for reports & charts."""
        from sqlalchemy import func
        from app.models.notification import Notification

        # Appointments by status
        appt_status = db.session.query(
            Appointment.status, func.count(Appointment.id)
        ).group_by(Appointment.status).all()

        # Urgency distribution from symptom records
        urgency_dist = db.session.query(
            SymptomRecord.urgency_level, func.count(SymptomRecord.id)
        ).group_by(SymptomRecord.urgency_level).all()

        # Monthly appointment counts (last 6 months)
        from datetime import datetime, timedelta
        monthly = {}
        today = datetime.utcnow().date()
        for i in range(5, -1, -1):
            month_start = (today.replace(day=1) - timedelta(days=i * 30)).replace(day=1)
            month_end_approx = month_start.replace(day=28) + timedelta(days=4)
            month_end = month_end_approx.replace(day=1) - timedelta(days=1)
            count = Appointment.query.filter(
                Appointment.date >= month_start,
                Appointment.date <= month_end
            ).count()
            monthly[month_start.strftime('%b %Y')] = count

        return {
            'appointmentsByStatus': {s: c for s, c in appt_status},
            'urgencyDistribution': {u: c for u, c in urgency_dist},
            'monthlyAppointments': monthly,
            'totalNotifications': Notification.query.count(),
            'unreadNotifications': Notification.query.filter_by(is_read=False).count(),
        }

    @staticmethod
    def get_audit_log(page=1, per_page=25):
        """Return a paginated list of audit log entries."""
        from app.models.audit_log import AuditLog
        return AuditLog.query.order_by(
            AuditLog.timestamp.desc()
        ).paginate(page=page, per_page=per_page, error_out=False)

    @staticmethod
    def log_action(admin_id, action, target_type=None, target_id=None, details=None):
        """Record an admin action in the audit log."""
        from app.models.audit_log import AuditLog
        entry = AuditLog(
            admin_id=admin_id,
            action=action,
            target_type=target_type,
            target_id=target_id,
            details=details,
        )
        db.session.add(entry)
        db.session.commit()
        return entry
