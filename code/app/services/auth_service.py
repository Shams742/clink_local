"""
CLINK — Authentication Service
Handles registration, login, and role-based access control.
"""
import re
from datetime import date, datetime
import bcrypt
from app.extensions import db
from app.models.patient import Patient
from app.models.doctor import Doctor
from app.models.admin import Admin


class AuthService:
    """Service for authentication and user validation."""

    # --- Validation helpers (NFR-002 to NFR-005) ---

    @staticmethod
    def validate_email(email):
        """NFR-002: Accept only valid email formats."""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not email or not re.match(pattern, email):
            return False, 'Please enter a valid email address.'
        return True, None

    @staticmethod
    def validate_password(password):
        """NFR-003: At least 1 number, 1 special char, min 6 chars."""
        if not password or len(password) < 6:
            return False, 'Password must be at least 6 characters long.'
        if not re.search(r'\d', password):
            return False, 'Password must contain at least one number.'
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            return False, 'Password must contain at least one special character.'
        return True, None

    @staticmethod
    def validate_name(name):
        """NFR-004: Not blank, only alphabetic + non-consecutive spaces."""
        if not name or not name.strip():
            return False, 'Name cannot be blank.'
        if not re.match(r'^[a-zA-Z]+( [a-zA-Z]+)*$', name.strip()):
            return False, 'Name must contain only letters and single spaces.'
        return True, None

    @staticmethod
    def validate_phone(phone):
        """NFR-005: Only numeric values with valid local format."""
        if not phone:
            return False, 'Phone number is required.'
        cleaned = phone.replace('+', '').replace('-', '').replace(' ', '')
        if not cleaned.isdigit() or len(cleaned) < 8 or len(cleaned) > 15:
            return False, 'Please enter a valid phone number (8-15 digits).'
        return True, None

    @staticmethod
    def validate_gender(gender):
        """Validate gender is Male or Female."""
        if not gender:
            return False, 'Gender is required.'
        if gender not in ('Male', 'Female'):
            return False, 'Gender must be Male or Female.'
        return True, None

    @staticmethod
    def validate_dob(dob_str):
        """Validate date of birth is a valid past date."""
        if not dob_str:
            return False, 'Date of birth is required.'
        try:
            dob = datetime.strptime(dob_str, '%Y-%m-%d').date()
        except (ValueError, TypeError):
            return False, 'Please enter a valid date of birth (YYYY-MM-DD).'
        if dob >= date.today():
            return False, 'Date of birth must be in the past.'
        return True, None

    @staticmethod
    def hash_password(password):
        """Hash password using bcrypt."""
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    @staticmethod
    def check_password(password, hashed):
        """Verify password against bcrypt hash."""
        return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

    @classmethod
    def register_patient(cls, name, email, phone, password, gender, dob):
        """
        UC001 — Register: Create a new patient account.
        Returns (patient, error_message).
        """
        # Validate all fields
        valid, err = cls.validate_name(name)
        if not valid:
            return None, err
        valid, err = cls.validate_email(email)
        if not valid:
            return None, err
        valid, err = cls.validate_phone(phone)
        if not valid:
            return None, err
        valid, err = cls.validate_password(password)
        if not valid:
            return None, err
        valid, err = cls.validate_gender(gender)
        if not valid:
            return None, err
        valid, err = cls.validate_dob(dob)
        if not valid:
            return None, err

        # Check duplicate email across all roles
        if Patient.query.filter_by(email=email).first():
            return None, 'An account with this email already exists.'
        if Doctor.query.filter_by(email=email).first():
            return None, 'An account with this email already exists.'
        if Admin.query.filter_by(email=email).first():
            return None, 'An account with this email already exists.'

        patient = Patient(
            name=name.strip(),
            email=email.strip().lower(),
            phone=phone.strip(),
            password=cls.hash_password(password),
            gender=gender,
            dob=datetime.strptime(dob, '%Y-%m-%d').date(),
        )
        db.session.add(patient)
        db.session.commit()
        return patient, None

    @classmethod
    def authenticate(cls, email, password):
        """
        Login: Authenticate user by email and password.
        Returns (user, role, error_message).
        """
        if not email or not password:
            return None, None, 'Email and password are required.'

        email = email.strip().lower()

        # Check each role table
        patient = Patient.query.filter_by(email=email).first()
        if patient and patient.account_status == 'active' and cls.check_password(password, patient.password):
            return patient, 'patient', None

        doctor = Doctor.query.filter_by(email=email).first()
        if doctor and doctor.account_status == 'active' and cls.check_password(password, doctor.password):
            return doctor, 'doctor', None

        admin = Admin.query.filter_by(email=email).first()
        if admin and cls.check_password(password, admin.password):
            return admin, 'admin', None

        return None, None, 'Invalid email or password.'

    @staticmethod
    def get_user_by_id(user_id_str):
        """Load user from composite ID (e.g. 'patient-5')."""
        try:
            role, uid = user_id_str.split('-', 1)
            uid = int(uid)
        except (ValueError, AttributeError):
            return None

        if role == 'patient':
            return Patient.query.get(uid)
        elif role == 'doctor':
            return Doctor.query.get(uid)
        elif role == 'admin':
            return Admin.query.get(uid)
        return None
