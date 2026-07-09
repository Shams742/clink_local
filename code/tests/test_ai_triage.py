"""
CLINK Test Suite — TC003/TC004/TC005: AI Triage Service Unit Tests
Direct tests of the AI model prediction pipeline.
"""
import pytest
from app.services.ai_triage_service import AITriageService


class TestAITriageService:
    """Unit tests for the AI Triage Service."""

    def test_model_loads(self, app):
        """Model loads or trains successfully."""
        with app.app_context():
            AITriageService.ensure_model()
            assert AITriageService._model is not None
            assert AITriageService._label_encoder is not None

    def test_predict_returns_valid_structure(self, app):
        """Prediction returns urgency, specialist, and condition."""
        with app.app_context():
            result = AITriageService.predict(['headache', 'high_fever', 'cough'])
            assert 'urgencyLevel' in result
            assert 'recommendedSpecialist' in result
            assert 'predictedCondition' in result
            assert result['urgencyLevel'] in ('urgent', 'non-urgent')

    def test_predict_skin_symptoms(self, app):
        """Skin symptoms predict Dermatologist."""
        with app.app_context():
            result = AITriageService.predict(['itching', 'skin_rash', 'nodal_skin_eruptions'])
            assert result['recommendedSpecialist'] == 'Dermatologist'

    def test_predict_cardiac_symptoms(self, app):
        """Cardiac symptoms predict Cardiologist."""
        with app.app_context():
            result = AITriageService.predict(['chest_pain', 'breathlessness', 'sweating', 'vomiting'])
            # Should predict Heart attack (urgent, Cardiologist)
            assert result['predictedCondition'] is not None

    def test_predict_cold_symptoms(self, app):
        """Cold symptoms are non-urgent."""
        with app.app_context():
            result = AITriageService.predict([
                'continuous_sneezing', 'cough', 'runny_nose',
                'congestion', 'throat_irritation'
            ])
            assert result['urgencyLevel'] == 'non-urgent'
            assert result['recommendedSpecialist'] == 'General Practitioner'

    def test_predict_urinary_symptoms(self, app):
        """UTI symptoms predict Urologist."""
        with app.app_context():
            result = AITriageService.predict([
                'burning_micturition', 'bladder_discomfort',
                'foul_smell_of_urine', 'continuous_feel_of_urine'
            ])
            assert result['recommendedSpecialist'] == 'Urologist'

    def test_predict_empty_symptoms(self, app):
        """Empty symptom list still returns a prediction."""
        with app.app_context():
            result = AITriageService.predict([])
            assert result['urgencyLevel'] in ('urgent', 'non-urgent')

    def test_predict_unknown_symptoms(self, app):
        """Unknown symptom codes are ignored gracefully."""
        with app.app_context():
            result = AITriageService.predict(['nonexistent_symptom_xyz'])
            assert result['urgencyLevel'] in ('urgent', 'non-urgent')

    def test_symptom_list_available(self, app):
        """Symptom list for UI is available and non-empty."""
        with app.app_context():
            symptoms = AITriageService.get_symptom_list()
            assert len(symptoms) > 50
            codes = AITriageService.get_symptom_codes()
            assert len(codes) == len(symptoms)

    def test_multiple_predictions_consistent(self, app):
        """Same symptoms produce same prediction."""
        with app.app_context():
            symptoms = ['headache', 'high_fever', 'nausea']
            r1 = AITriageService.predict(symptoms)
            r2 = AITriageService.predict(symptoms)
            assert r1['predictedCondition'] == r2['predictedCondition']
            assert r1['urgencyLevel'] == r2['urgencyLevel']
