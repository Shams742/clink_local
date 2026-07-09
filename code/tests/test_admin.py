"""
CLINK Test Suite — TC011/TC012: Admin Management (FR-011, FR-012 / UC011, UC012)
Tests user management and schedule configuration.
"""
import pytest
from tests.conftest import login_as


class TestTC011ManageUsers:
    """TC011 — Manage Users (FR-011 / UC011)."""

    # TC011_01: Admin can create a doctor
    def test_create_doctor(self, client, db, seed_admin):
        """Admin can create a new doctor account."""
        login_as(client, 'admin@test.com')
        resp = client.post('/api/admin/users/doctor', json={
            'name': 'New Doctor',
            'email': 'newdoc@test.com',
            'password': 'Test@123',
            'specialization': 'Cardiologist',
        })
        data = resp.get_json()
        assert resp.status_code == 200
        assert data['success'] is True
        assert data['doctor']['specialization'] == 'Cardiologist'

    def test_create_doctor_duplicate_email(self, client, db, seed_admin, seed_doctor):
        """Cannot create doctor with existing email."""
        login_as(client, 'admin@test.com')
        resp = client.post('/api/admin/users/doctor', json={
            'name': 'Duplicate Doctor',
            'email': 'doctor@test.com',
            'password': 'Test@123',
            'specialization': 'Neurologist',
        })
        assert resp.status_code == 400

    def test_list_users(self, client, db, seed_admin, seed_patient, seed_doctor):
        """Admin can list all users."""
        login_as(client, 'admin@test.com')
        resp = client.get('/api/admin/users')
        data = resp.get_json()
        assert data['success'] is True
        assert len(data['patients']) >= 1
        assert len(data['doctors']) >= 1

    def test_deactivate_patient(self, client, db, seed_admin, seed_patient):
        """Admin can deactivate a patient account."""
        login_as(client, 'admin@test.com')
        resp = client.put(f'/api/admin/users/{seed_patient.id}/deactivate', json={
            'role': 'patient',
        })
        data = resp.get_json()
        assert data['success'] is True

    def test_activate_patient(self, client, db, seed_admin, seed_patient):
        """Admin can reactivate a patient account."""
        login_as(client, 'admin@test.com')
        # Deactivate first
        client.put(f'/api/admin/users/{seed_patient.id}/deactivate', json={'role': 'patient'})
        # Reactivate
        resp = client.put(f'/api/admin/users/{seed_patient.id}/activate', json={'role': 'patient'})
        data = resp.get_json()
        assert data['success'] is True

    def test_admin_stats(self, client, db, seed_admin, seed_patient, seed_doctor):
        """Admin can see dashboard stats."""
        login_as(client, 'admin@test.com')
        resp = client.get('/api/admin/stats')
        data = resp.get_json()
        assert data['success'] is True
        assert data['stats']['totalPatients'] >= 1
        assert data['stats']['totalDoctors'] >= 1


class TestTC012ConfigureSchedules:
    """TC012 — Configure Schedules (FR-012 / UC012)."""

    # TC012_01: Admin can update doctor availability
    def test_update_availability(self, client, db, seed_admin, seed_doctor):
        """Admin can set doctor as unavailable."""
        login_as(client, 'admin@test.com')
        resp = client.put(f'/api/admin/schedules/{seed_doctor.id}', json={
            'availability': 'unavailable',
        })
        data = resp.get_json()
        assert data['success'] is True
        assert data['doctor']['availability'] == 'unavailable'

    def test_update_availability_back(self, client, db, seed_admin, seed_doctor):
        """Admin can set doctor back to available."""
        login_as(client, 'admin@test.com')
        client.put(f'/api/admin/schedules/{seed_doctor.id}', json={'availability': 'unavailable'})
        resp = client.put(f'/api/admin/schedules/{seed_doctor.id}', json={'availability': 'available'})
        data = resp.get_json()
        assert data['doctor']['availability'] == 'available'

    def test_invalid_availability(self, client, db, seed_admin, seed_doctor):
        """Invalid availability value is rejected."""
        login_as(client, 'admin@test.com')
        resp = client.put(f'/api/admin/schedules/{seed_doctor.id}', json={
            'availability': 'maybe',
        })
        assert resp.status_code == 400


class TestRBAC:
    """NFR-019: Role-based access control."""

    def test_patient_cannot_access_doctor_api(self, client, db, seed_patient):
        """Patient cannot access doctor endpoints."""
        login_as(client, 'patient@test.com')
        resp = client.get('/api/doctor/cases')
        # Should redirect to login or return error
        assert resp.status_code in (302, 401, 403)

    def test_patient_cannot_access_admin_api(self, client, db, seed_patient):
        """Patient cannot access admin endpoints."""
        login_as(client, 'patient@test.com')
        resp = client.get('/api/admin/users')
        assert resp.status_code in (302, 401, 403)

    def test_doctor_cannot_access_admin_api(self, client, db, seed_doctor):
        """Doctor cannot access admin endpoints."""
        login_as(client, 'doctor@test.com')
        resp = client.get('/api/admin/users')
        assert resp.status_code in (302, 401, 403)

    def test_unauthenticated_access_blocked(self, client, db):
        """Unauthenticated users cannot access protected routes."""
        resp = client.get('/api/patient/records')
        assert resp.status_code in (302, 401)
