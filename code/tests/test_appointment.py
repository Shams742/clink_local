"""
CLINK Test Suite — TC007: Appointment Booking (FR-007 / UC007)
Tests appointment slot generation, booking, and conflict detection.
"""
import pytest
from datetime import date, timedelta
from tests.conftest import login_as
from app.models import SymptomRecord


class TestTC007BookAppointment:
    """TC007 — Book Appointment (FR-007 / UC007)."""

    def _create_record_for_patient(self, client, db, seed_patient, seed_doctor):
        """Helper: submit symptoms and return record ID."""
        login_as(client, 'patient@test.com')
        resp = client.post('/api/patient/symptoms', json={
            'symptoms': ['headache', 'high_fever'],
            'details': 'Test',
        })
        data = resp.get_json()
        return data['record']['id'], seed_doctor.id

    # TC007_01: Successful appointment booking
    def test_book_appointment_success(self, client, db, seed_patient, seed_doctor):
        """Patient can book an appointment with available slot."""
        record_id, doctor_id = self._create_record_for_patient(
            client, db, seed_patient, seed_doctor
        )

        # Get available slots
        resp = client.get(f'/api/appointment/slots?doctor_id={doctor_id}&urgency=non-urgent')
        data = resp.get_json()
        assert data['success'] is True
        assert len(data['slots']) > 0

        slot = data['slots'][0]

        # Book the slot
        resp2 = client.post('/api/appointment/book', json={
            'doctorId': doctor_id,
            'recordId': record_id,
            'date': slot['date'],
            'time': slot['time'],
        })
        data2 = resp2.get_json()
        assert resp2.status_code == 200
        assert data2['success'] is True
        assert data2['appointment']['status'] == 'scheduled'

    # TC007_02: Double booking prevented
    def test_book_appointment_conflict(self, client, db, seed_patient, seed_doctor):
        """Same slot cannot be booked twice."""
        record_id, doctor_id = self._create_record_for_patient(
            client, db, seed_patient, seed_doctor
        )

        resp = client.get(f'/api/appointment/slots?doctor_id={doctor_id}&urgency=non-urgent')
        slot = resp.get_json()['slots'][0]

        # First booking
        client.post('/api/appointment/book', json={
            'doctorId': doctor_id,
            'recordId': record_id,
            'date': slot['date'],
            'time': slot['time'],
        })

        # Submit another record for second booking attempt
        resp2 = client.post('/api/patient/symptoms', json={
            'symptoms': ['cough'],
            'details': '',
        })
        record_id_2 = resp2.get_json()['record']['id']

        # Try same slot
        resp3 = client.post('/api/appointment/book', json={
            'doctorId': doctor_id,
            'recordId': record_id_2,
            'date': slot['date'],
            'time': slot['time'],
        })
        data3 = resp3.get_json()
        assert resp3.status_code == 400
        assert 'not available' in data3['error'].lower() or 'no longer' in data3['error'].lower()

    def test_get_available_slots(self, client, db, seed_patient, seed_doctor):
        """Available slots are returned for a doctor."""
        login_as(client, 'patient@test.com')
        resp = client.get(f'/api/appointment/slots?doctor_id={seed_doctor.id}&urgency=non-urgent')
        data = resp.get_json()
        assert data['success'] is True
        assert isinstance(data['slots'], list)
        if len(data['slots']) > 0:
            assert 'date' in data['slots'][0]
            assert 'time' in data['slots'][0]

    def test_get_patient_appointments(self, client, db, seed_patient, seed_doctor):
        """Patient can list their appointments."""
        record_id, doctor_id = self._create_record_for_patient(
            client, db, seed_patient, seed_doctor
        )

        # Book an appointment
        resp = client.get(f'/api/appointment/slots?doctor_id={doctor_id}&urgency=non-urgent')
        slot = resp.get_json()['slots'][0]
        client.post('/api/appointment/book', json={
            'doctorId': doctor_id,
            'recordId': record_id,
            'date': slot['date'],
            'time': slot['time'],
        })

        # List appointments
        resp2 = client.get('/api/appointment/patient')
        data = resp2.get_json()
        assert data['success'] is True
        assert len(data['appointments']) >= 1
