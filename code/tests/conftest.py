"""
CLINK — Test Configuration
Shared fixtures for the test suite.
"""
import sys
import os
from datetime import date
import pytest

# Ensure the app is importable
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app import create_app
from app.extensions import db as _db
from app.models import Admin, Patient, Doctor, SymptomRecord, Appointment, Notification
from app.services.auth_service import AuthService


@pytest.fixture(scope='session')
def app():
    """Create application for testing."""
    app = create_app('testing')
    with app.app_context():
        _db.create_all()
        yield app
        _db.drop_all()


@pytest.fixture(scope='function')
def db(app):
    """Fresh database for each test."""
    with app.app_context():
        _db.create_all()
        yield _db
        _db.session.rollback()
        for table in reversed(_db.metadata.sorted_tables):
            _db.session.execute(table.delete())
        _db.session.commit()


@pytest.fixture
def client(app):
    """Flask test client."""
    return app.test_client()


@pytest.fixture
def seed_admin(db):
    """Create a test admin."""
    admin = Admin(
        name='Test Admin',
        email='admin@test.com',
        password=AuthService.hash_password('Test@123'),
        role='admin',
        access_level='full'
    )
    db.session.add(admin)
    db.session.commit()
    return admin


@pytest.fixture
def seed_doctor(db):
    """Create a test doctor."""
    doctor = Doctor(
        name='Test Doctor',
        email='doctor@test.com',
        password=AuthService.hash_password('Test@123'),
        specialization='General Practitioner',
        availability='available',
    )
    db.session.add(doctor)
    db.session.commit()
    return doctor


@pytest.fixture
def seed_patient(db):
    """Create a test patient."""
    patient = Patient(
        name='Test Patient',
        email='patient@test.com',
        phone='96512345678',
        password=AuthService.hash_password('Test@123'),
        gender='Male',
        dob=date(1990, 5, 15),
    )
    db.session.add(patient)
    db.session.commit()
    return patient


def login_as(client, email, password='Test@123'):
    """Helper to log in via API and return response."""
    return client.post('/api/auth/login',
                       json={'email': email, 'password': password},
                       content_type='application/json')
