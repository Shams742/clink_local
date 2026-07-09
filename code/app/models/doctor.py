"""
CLINK — Doctor Entity
Stores doctor details, specialisation, and availability.
"""
from flask_login import UserMixin
from app.extensions import db


class Doctor(UserMixin, db.Model):
    __tablename__ = 'doctors'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    specialization = db.Column(db.String(100), nullable=False)
    availability = db.Column(db.String(50), default='available')  # available / unavailable
    account_status = db.Column(db.String(20), default='active')
    role = db.Column(db.String(10), default='doctor')
    # JSON string: e.g. '{"start": 8, "end": 17}' — clinic hours override
    schedule_hours = db.Column(db.String(50), default='{"start": 8, "end": 17}')

    # Relationships
    appointments = db.relationship('Appointment', backref='doctor', lazy='dynamic')
    assigned_records = db.relationship('SymptomRecord', backref='assigned_doctor', lazy='dynamic')
    notifications = db.relationship(
        'Notification',
        primaryjoin="and_(Doctor.id == foreign(Notification.user_id), Notification.user_role == 'doctor')",
        lazy='dynamic',
        viewonly=True
    )

    def get_id(self):
        return f"doctor-{self.id}"

    def to_dict(self):
        import json
        try:
            hours = json.loads(self.schedule_hours or '{"start": 8, "end": 17}')
        except Exception:
            hours = {'start': 8, 'end': 17}
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'specialization': self.specialization,
            'availability': self.availability,
            'accountStatus': self.account_status,
            'role': self.role,
            'scheduleHours': hours,
        }

    def __repr__(self):
        return f'<Doctor {self.name} ({self.specialization})>'
