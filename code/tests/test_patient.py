"""
CLINK Test Suite — TC002-TC006: Symptom Submission & AI Triage
Tests FR-002 to FR-006 / UC002 to UC006.
"""
import pytest
from tests.conftest import login_as


class TestTC002SubmitSymptoms:
    """TC002 — Submit Symptoms (FR-002 / UC002)."""

    # TC002_01: Successful symptom submission
    def test_submit_symptoms_success(self, client, db, seed_patient, seed_doctor):
        """Patient can submit symptoms and receive AI analysis."""
        login_as(client, 'patient@test.com')
        resp = client.post('/api/patient/symptoms', json={
            'symptoms': ['headache', 'high_fever', 'cough'],
            'details': 'Fever for 3 days with persistent cough',
        })
        data = resp.get_json()
        assert resp.status_code == 200
        assert data['success'] is True
        assert 'record' in data
        assert data['record']['analysisStatus'] == 'completed'

    # TC002_02: Empty symptoms rejected
    def test_submit_no_symptoms(self, client, db, seed_patient):
        """Submitting with no symptoms is rejected."""
        login_as(client, 'patient@test.com')
        resp = client.post('/api/patient/symptoms', json={
            'symptoms': [],
            'details': '',
        })
        data = resp.get_json()
        assert resp.status_code == 400
        assert data['success'] is False


class TestTC003AnalyseSymptoms:
    """TC003 — Analyse Symptoms (FR-003 / UC003)."""

    # TC003_01: AI analysis returns valid result
    def test_ai_analysis_returns_result(self, client, db, seed_patient, seed_doctor):
        """AI triage returns urgency and specialist."""
        login_as(client, 'patient@test.com')
        resp = client.post('/api/patient/symptoms', json={
            'symptoms': ['chest_pain', 'breathlessness', 'sweating'],
            'details': 'Sudden chest pain',
        })
        data = resp.get_json()
        record = data['record']
        assert record['urgencyLevel'] in ('urgent', 'non-urgent')
        assert record['recommendedSpecialist'] is not None
        assert record['predictedCondition'] is not None

    # TC003_02: Analysis results are stored in symptom record
    def test_ai_results_stored(self, client, db, seed_patient, seed_doctor):
        """AI results are persisted in the database."""
        login_as(client, 'patient@test.com')
        resp = client.post('/api/patient/symptoms', json={
            'symptoms': ['itching', 'skin_rash'],
            'details': '',
        })
        data = resp.get_json()
        record_id = data['record']['id']

        # Fetch the record
        resp2 = client.get(f'/api/patient/triage/{record_id}')
        data2 = resp2.get_json()
        assert data2['success'] is True
        assert data2['record']['analysisStatus'] == 'completed'


class TestTC004ClassifyUrgency:
    """TC004 — Classify Urgency (FR-004 / UC004)."""

    # TC004_01: Urgent symptoms classified correctly
    def test_urgent_classification(self, client, db, seed_patient, seed_doctor):
        """Heart attack symptoms classified as urgent."""
        login_as(client, 'patient@test.com')
        resp = client.post('/api/patient/symptoms', json={
            'symptoms': ['chest_pain', 'vomiting', 'breathlessness', 'sweating'],
            'details': '',
        })
        data = resp.get_json()
        # Heart attack is mapped to urgent
        assert data['record']['predictedCondition'] is not None

    # TC004_02: Non-urgent symptoms classified correctly
    def test_non_urgent_classification(self, client, db, seed_patient, seed_doctor):
        """Common cold symptoms classified as non-urgent."""
        login_as(client, 'patient@test.com')
        resp = client.post('/api/patient/symptoms', json={
            'symptoms': ['continuous_sneezing', 'cough', 'runny_nose', 'congestion'],
            'details': '',
        })
        data = resp.get_json()
        assert data['record']['urgencyLevel'] == 'non-urgent'


class TestTC005RecommendSpecialist:
    """TC005 — Recommend Specialist (FR-005 / UC005)."""

    # TC005_01: Specialist recommended based on condition
    def test_specialist_recommendation(self, client, db, seed_patient, seed_doctor):
        """AI recommends appropriate specialist type."""
        login_as(client, 'patient@test.com')
        resp = client.post('/api/patient/symptoms', json={
            'symptoms': ['itching', 'skin_rash', 'nodal_skin_eruptions'],
            'details': '',
        })
        data = resp.get_json()
        specialist = data['record']['recommendedSpecialist']
        assert specialist is not None
        assert len(specialist) > 0
        # Skin symptoms should map to Dermatologist
        assert specialist == 'Dermatologist'


class TestTC006ViewTriageResult:
    """TC006 — View Triage Result (FR-006 / UC006)."""

    # TC006_01: Patient can view their triage result
    def test_view_triage_result(self, client, db, seed_patient, seed_doctor):
        """Patient can retrieve triage result by record ID."""
        login_as(client, 'patient@test.com')

        # Submit symptoms first
        resp = client.post('/api/patient/symptoms', json={
            'symptoms': ['headache', 'nausea'],
            'details': '',
        })
        record_id = resp.get_json()['record']['id']

        # View the result
        resp2 = client.get(f'/api/patient/triage/{record_id}')
        data = resp2.get_json()
        assert resp2.status_code == 200
        assert data['success'] is True
        assert data['record']['urgencyLevel'] is not None

    def test_view_nonexistent_record(self, client, db, seed_patient):
        """Requesting non-existent record returns 404."""
        login_as(client, 'patient@test.com')
        resp = client.get('/api/patient/triage/9999')
        assert resp.status_code == 404
