"""
CLINK — Patient Service
Handles symptom submission and triage flow.
"""
from app.extensions import db
from app.models.symptom_record import SymptomRecord
from app.models.doctor import Doctor
from app.services.ai_triage_service import AITriageService


class PatientService:
    """Business logic for patient operations."""

    @staticmethod
    def submit_symptoms(patient_id, symptom_details, symptoms_list):
        """
        UC002-UC006: Submit symptoms → AI analysis → urgency classification 
        → specialist recommendation → store result.
        """
        # Create symptom record
        record = SymptomRecord(
            patient_id=patient_id,
            symptom_details=symptom_details,
            symptoms_list=','.join(symptoms_list),
            analysis_status='pending'
        )
        db.session.add(record)
        db.session.flush()  # get ID

        try:
            # UC003: Send to AI Triage Service
            result = AITriageService.predict(symptoms_list)

            record.urgency_level = result['urgencyLevel']
            record.recommended_specialist = result['recommendedSpecialist']
            record.predicted_condition = result['predictedCondition']
            record.analysis_status = 'completed'

            # Auto-assign a doctor based on specialist recommendation
            doctor = Doctor.query.filter_by(
                specialization=result['recommendedSpecialist'],
                availability='available',
                account_status='active'
            ).first()

            if not doctor:
                # Fallback: assign any available doctor
                doctor = Doctor.query.filter_by(
                    availability='available',
                    account_status='active'
                ).first()

            if doctor:
                record.doctor_id = doctor.id

            db.session.commit()
            return record, None

        except Exception as e:
            record.analysis_status = 'failed'
            db.session.commit()
            return None, f'AI analysis failed: {str(e)}. Please try again later.'

    @staticmethod
    def get_patient_records(patient_id):
        """Get all symptom records for a patient."""
        return SymptomRecord.query.filter_by(patient_id=patient_id)\
            .order_by(SymptomRecord.created_at.desc()).all()

    @staticmethod
    def get_record(record_id, patient_id=None):
        """Get a specific symptom record."""
        query = SymptomRecord.query.filter_by(id=record_id)
        if patient_id:
            query = query.filter_by(patient_id=patient_id)
        return query.first()
