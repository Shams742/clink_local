"""
CLINK Test Suite — TC001: Patient Registration (FR-001 / UC001)
Tests patient account creation with validation rules NFR-002 to NFR-005.
"""
import pytest
from tests.conftest import login_as


class TestTC001Registration:
    """TC001 — Patient Registration."""

    # TC001_01: Successful registration
    def test_register_success(self, client, db):
        """Valid registration creates account and auto-logs in."""
        resp = client.post('/api/auth/register', json={
            'name': 'Ahmad Salem',
            'email': 'ahmad@example.com',
            'phone': '96512345678',
            'password': 'Test@123',
            'gender': 'Male',
            'dob': '1990-06-15',
        })
        data = resp.get_json()
        assert resp.status_code == 200
        assert data['success'] is True
        assert 'redirect' in data

    # TC001_02: Duplicate email
    def test_register_duplicate_email(self, client, db, seed_patient):
        """Registration with existing email fails."""
        resp = client.post('/api/auth/register', json={
            'name': 'Another Person',
            'email': 'patient@test.com',  # already exists
            'phone': '96599999999',
            'password': 'Test@123',
            'gender': 'Female',
            'dob': '1985-01-20',
        })
        data = resp.get_json()
        assert resp.status_code == 400
        assert data['success'] is False
        assert 'already exists' in data['error']

    # NFR-002: Email validation
    def test_register_invalid_email(self, client, db):
        """Invalid email format is rejected."""
        resp = client.post('/api/auth/register', json={
            'name': 'Test User',
            'email': 'not-an-email',
            'phone': '96512345678',
            'password': 'Test@123',
            'gender': 'Male',
            'dob': '1990-01-01',
        })
        data = resp.get_json()
        assert resp.status_code == 400
        assert data['success'] is False

    # NFR-003: Password validation
    def test_register_weak_password_no_number(self, client, db):
        """Password without number is rejected."""
        resp = client.post('/api/auth/register', json={
            'name': 'Test User',
            'email': 'test@example.com',
            'phone': '96512345678',
            'password': 'abcdef@',
            'gender': 'Male',
            'dob': '1990-01-01',
        })
        data = resp.get_json()
        assert resp.status_code == 400
        assert 'number' in data['error'].lower()

    def test_register_weak_password_no_special(self, client, db):
        """Password without special character is rejected."""
        resp = client.post('/api/auth/register', json={
            'name': 'Test User',
            'email': 'test@example.com',
            'phone': '96512345678',
            'password': 'abcdef1',
            'gender': 'Male',
            'dob': '1990-01-01',
        })
        data = resp.get_json()
        assert resp.status_code == 400
        assert 'special' in data['error'].lower()

    def test_register_short_password(self, client, db):
        """Password under 6 characters is rejected."""
        resp = client.post('/api/auth/register', json={
            'name': 'Test User',
            'email': 'test@example.com',
            'phone': '96512345678',
            'password': 'Ab@1',
            'gender': 'Male',
            'dob': '1990-01-01',
        })
        data = resp.get_json()
        assert resp.status_code == 400

    # NFR-004: Name validation
    def test_register_blank_name(self, client, db):
        """Blank name is rejected."""
        resp = client.post('/api/auth/register', json={
            'name': '',
            'email': 'test@example.com',
            'phone': '96512345678',
            'password': 'Test@123',
            'gender': 'Male',
            'dob': '1990-01-01',
        })
        data = resp.get_json()
        assert resp.status_code == 400

    def test_register_name_with_numbers(self, client, db):
        """Name with numbers is rejected."""
        resp = client.post('/api/auth/register', json={
            'name': 'Test123',
            'email': 'test@example.com',
            'phone': '96512345678',
            'password': 'Test@123',
            'gender': 'Male',
            'dob': '1990-01-01',
        })
        data = resp.get_json()
        assert resp.status_code == 400

    # NFR-005: Phone validation
    def test_register_invalid_phone(self, client, db):
        """Non-numeric phone is rejected."""
        resp = client.post('/api/auth/register', json={
            'name': 'Test User',
            'email': 'test@example.com',
            'phone': 'not-a-phone',
            'password': 'Test@123',
            'gender': 'Male',
            'dob': '1990-01-01',
        })
        data = resp.get_json()
        assert resp.status_code == 400


class TestLogin:
    """Login tests for all roles."""

    def test_login_patient(self, client, db, seed_patient):
        """Patient can log in with correct credentials."""
        resp = login_as(client, 'patient@test.com')
        data = resp.get_json()
        assert resp.status_code == 200
        assert data['success'] is True
        assert data['role'] == 'patient'

    def test_login_doctor(self, client, db, seed_doctor):
        """Doctor can log in."""
        resp = login_as(client, 'doctor@test.com')
        data = resp.get_json()
        assert resp.status_code == 200
        assert data['role'] == 'doctor'

    def test_login_admin(self, client, db, seed_admin):
        """Admin can log in."""
        resp = login_as(client, 'admin@test.com')
        data = resp.get_json()
        assert resp.status_code == 200
        assert data['role'] == 'admin'

    def test_login_wrong_password(self, client, db, seed_patient):
        """Wrong password is rejected."""
        resp = login_as(client, 'patient@test.com', 'WrongPass@1')
        data = resp.get_json()
        assert resp.status_code == 401
        assert data['success'] is False

    def test_login_nonexistent_email(self, client, db):
        """Non-existent email is rejected."""
        resp = login_as(client, 'nobody@example.com')
        data = resp.get_json()
        assert resp.status_code == 401

    def test_logout(self, client, db, seed_patient):
        """Logout redirects to login."""
        login_as(client, 'patient@test.com')
        resp = client.get('/logout')
        assert resp.status_code == 302
