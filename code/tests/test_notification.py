"""
CLINK Test Suite — TC008: Notifications (FR-008 / UC008)
Tests notification creation, retrieval, and read status.
"""
import pytest
from tests.conftest import login_as
from app.services.notification_service import NotificationService


class TestTC008Notifications:
    """TC008 — Receive Notifications (FR-008 / UC008)."""

    # TC008_01: Notification created on appointment booking
    def test_notification_on_booking(self, client, db, seed_patient, seed_doctor):
        """Booking an appointment creates notifications for patient and doctor."""
        login_as(client, 'patient@test.com')

        # Submit symptoms and book
        resp = client.post('/api/patient/symptoms', json={
            'symptoms': ['headache', 'high_fever'],
            'details': '',
        })
        record_id = resp.get_json()['record']['id']

        slots_resp = client.get(f'/api/appointment/slots?doctor_id={seed_doctor.id}&urgency=non-urgent')
        slot = slots_resp.get_json()['slots'][0]

        client.post('/api/appointment/book', json={
            'doctorId': seed_doctor.id,
            'recordId': record_id,
            'date': slot['date'],
            'time': slot['time'],
        })

        # Check patient notifications
        resp2 = client.get('/api/patient/notifications')
        data = resp2.get_json()
        assert data['success'] is True
        assert len(data['notifications']) >= 1
        assert data['unreadCount'] >= 1

    def test_mark_notification_read(self, client, db, seed_patient):
        """Patient can mark a notification as read."""
        login_as(client, 'patient@test.com')

        # Create a notification directly
        with client.application.app_context():
            notif = NotificationService.create_notification(
                user_id=seed_patient.id,
                user_role='patient',
                message='Test notification',
                notification_type='info'
            )
            notif_id = notif.id

        resp = client.put(f'/api/patient/notifications/{notif_id}/read')
        assert resp.get_json()['success'] is True

    def test_mark_all_read(self, client, db, seed_patient):
        """Patient can mark all notifications as read."""
        login_as(client, 'patient@test.com')

        with client.application.app_context():
            for i in range(3):
                NotificationService.create_notification(
                    user_id=seed_patient.id,
                    user_role='patient',
                    message=f'Test notification {i}',
                )

        resp = client.put('/api/patient/notifications/read-all')
        assert resp.get_json()['success'] is True

        # Verify all read
        resp2 = client.get('/api/patient/notifications')
        assert resp2.get_json()['unreadCount'] == 0
