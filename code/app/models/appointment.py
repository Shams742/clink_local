"""
CLINK — Appointment Entity
Stores outpatient appointment details and status.
"""
from datetime import datetime
from app.extensions import db


class Appointment(db.Model):
    __tablename__ = 'appointments'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.id'), nullable=False)
    record_id = db.Column(db.Integer, db.ForeignKey('symptom_records.id'), nullable=True)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)
    status = db.Column(db.String(30), default='requested')
    # Status values: requested / scheduled / completed / cancelled
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'patientId': self.patient_id,
            'doctorId': self.doctor_id,
            'recordId': self.record_id,
            'date': self.date.isoformat() if self.date else None,
            'time': self.time.strftime('%H:%M') if self.time else None,
            'status': self.status,
            'createdAt': self.created_at.isoformat() if self.created_at else None,
            'doctor': self.doctor.to_dict() if self.doctor else None,
            'patient': self.patient.to_dict() if self.patient else None,
        }

    def __repr__(self):
        return f'<Appointment {self.id} - {self.date} {self.time}>'
