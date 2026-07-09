"""
CLINK — SymptomRecord Entity
Stores patient-submitted symptoms and AI urgency classification results.
"""
from datetime import datetime
from app.extensions import db


class SymptomRecord(db.Model):
    __tablename__ = 'symptom_records'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.id'), nullable=True)  # assigned after triage
    symptom_details = db.Column(db.Text, nullable=False)
    symptoms_list = db.Column(db.Text, nullable=True)       # comma-separated symptom codes
    urgency_level = db.Column(db.String(20), nullable=True)  # urgent / non-urgent
    recommended_specialist = db.Column(db.String(100), nullable=True)
    predicted_condition = db.Column(db.String(200), nullable=True)
    analysis_status = db.Column(db.String(20), default='pending')  # pending / completed / failed
    case_status = db.Column(db.String(30), default='new')  # new / in-review / consulted / closed
    consultation_notes = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationship
    appointment = db.relationship('Appointment', backref='symptom_record', uselist=False)

    def to_dict(self):
        return {
            'id': self.id,
            'patientId': self.patient_id,
            'doctorId': self.doctor_id,
            'symptomDetails': self.symptom_details,
            'symptomsList': self.symptoms_list.split(',') if self.symptoms_list else [],
            'urgencyLevel': self.urgency_level,
            'recommendedSpecialist': self.recommended_specialist,
            'predictedCondition': self.predicted_condition,
            'analysisStatus': self.analysis_status,
            'caseStatus': self.case_status,
            'consultationNotes': self.consultation_notes,
            'createdAt': self.created_at.isoformat() if self.created_at else None,
            'patient': self.patient.to_dict() if self.patient else None,
        }

    def __repr__(self):
        return f'<SymptomRecord {self.id} - {self.urgency_level}>'
