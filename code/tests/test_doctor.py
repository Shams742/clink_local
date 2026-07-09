"""
CLINK Test Suite — TC009/TC010: Doctor Case Management (FR-009, FR-010 / UC009, UC010)
Tests doctor dashboard cases and case status updates.
"""
import pytest
from tests.conftest import login_as
from app.models import SymptomRecord


class TestTC009ViewPatientCases:
    """TC009 — View Patient Cases (FR-009 / UC009)."""

    def _setup_case(self, client, db, seed_patient, seed_doctor):
        """Helper: create a patient case assigned to the doctor."""
        login_as(client, 'patient@test.com')
        resp = client.post('/api/patient/symptoms', json={
            'symptoms': ['headache', 'high_fever'],
            'details': 'Test case',
        })
        record = resp.get_json()['record']

        # Manually assign doctor if not auto-assigned
        with client.application.app_context():
            sr = SymptomRecord.query.get(record['id'])
            if not sr.doctor_id:
                sr.doctor_id = seed_doctor.id
                db.session.commit()

        return record['id']

    # TC009_01: Doctor sees assigned cases
    def test_view_assigned_cases(self, client, db, seed_patient, seed_doctor):
        """Doctor can view their assigned patient cases."""
        record_id = self._setup_case(client, db, seed_patient, seed_doctor)

        # Login as doctor
        login_as(client, 'doctor@test.com')
        resp = client.get('/api/doctor/cases')
        data = resp.get_json()
        assert data['success'] is True
        assert len(data['cases']) >= 1

    # TC009_02: Empty cases
    def test_empty_dashboard(self, client, db, seed_doctor):
        """Doctor with no cases sees empty list."""
        login_as(client, 'doctor@test.com')
        resp = client.get('/api/doctor/cases')
        data = resp.get_json()
        assert data['success'] is True
        assert len(data['cases']) == 0


class TestTC010UpdateCaseStatus:
    """TC010 — Update Case Status (FR-010 / UC010)."""

    def _setup_case(self, client, db, seed_patient, seed_doctor):
        """Helper: create and assign a case."""
        login_as(client, 'patient@test.com')
        resp = client.post('/api/patient/symptoms', json={
            'symptoms': ['headache', 'nausea'],
            'details': '',
        })
        record_id = resp.get_json()['record']['id']
        with client.application.app_context():
            sr = SymptomRecord.query.get(record_id)
            if not sr.doctor_id:
                sr.doctor_id = seed_doctor.id
                db.session.commit()
        return record_id

    # TC010_01: Update status successfully
    def test_update_case_status(self, client, db, seed_patient, seed_doctor):
        """Doctor can update case status."""
        record_id = self._setup_case(client, db, seed_patient, seed_doctor)

        login_as(client, 'doctor@test.com')
        resp = client.put(f'/api/doctor/cases/{record_id}/status', json={
            'status': 'in-review',
            'notes': 'Reviewing symptoms. Will schedule consultation.',
        })
        data = resp.get_json()
        assert resp.status_code == 200
        assert data['success'] is True
        assert data['case']['caseStatus'] == 'in-review'

    # TC010_02: Invalid status rejected
    def test_update_invalid_status(self, client, db, seed_patient, seed_doctor):
        """Invalid status value is rejected."""
        record_id = self._setup_case(client, db, seed_patient, seed_doctor)

        login_as(client, 'doctor@test.com')
        resp = client.put(f'/api/doctor/cases/{record_id}/status', json={
            'status': 'invalid-status',
        })
        data = resp.get_json()
        assert resp.status_code == 400
        assert data['success'] is False

    def test_view_case_details(self, client, db, seed_patient, seed_doctor):
        """Doctor can view full case details including AI results."""
        record_id = self._setup_case(client, db, seed_patient, seed_doctor)

        login_as(client, 'doctor@test.com')
        resp = client.get(f'/api/doctor/cases/{record_id}')
        data = resp.get_json()
        assert data['success'] is True
        assert 'urgencyLevel' in data['case']
        assert 'patient' in data['case']

    def test_doctor_stats(self, client, db, seed_patient, seed_doctor):
        """Doctor can retrieve dashboard statistics."""
        self._setup_case(client, db, seed_patient, seed_doctor)

        login_as(client, 'doctor@test.com')
        resp = client.get('/api/doctor/stats')
        data = resp.get_json()
        assert data['success'] is True
        assert 'totalCases' in data['stats']
        assert data['stats']['totalCases'] >= 1
