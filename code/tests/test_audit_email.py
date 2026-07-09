"""
Tests for new CLINK features: Audit logging, schedule slot configure API, and simulated email log.
"""
import pytest
import json
from tests.conftest import login_as
from app.models.audit_log import AuditLog
from app.services.notification_service import NotificationService, EMAIL_LOG


def test_audit_log_recorded(client, db, seed_admin):
    """Admin actions generate AuditLog entries."""
    login_as(client, 'admin@test.com')
    
    # 1. Create doctor
    resp = client.post('/api/admin/users/doctor', json={
        'name': 'Test Audit Doctor',
        'email': 'auditdoc@test.com',
        'password': 'Test@123',
        'specialization': 'General Practitioner',
    })
    assert resp.status_code == 200

    # Verify audit log exists
    audit_entry = AuditLog.query.filter_by(action='create_doctor').first()
    assert audit_entry is not None
    assert 'Test Audit Doctor' in audit_entry.details


def test_email_simulation(client, db, seed_admin):
    """Simulated emails are appended to EMAIL_LOG and physical file."""
    # Send a simulated email
    email = NotificationService.simulate_email(
        to='test@example.com',
        subject='Test Subject',
        body='Test Body'
    )
    assert email['to'] == 'test@example.com'
    assert email['subject'] == 'Test Subject'
    assert email['body'] == 'Test Body'
    
    # Check that it exists in the list
    assert any(e['to'] == 'test@example.com' for e in EMAIL_LOG)


def test_configure_schedule_hours(client, db, seed_admin, seed_doctor):
    """Admin can configure doctor schedule working hours."""
    login_as(client, 'admin@test.com')
    
    resp = client.put(f'/api/admin/schedules/{seed_doctor.id}/hours', json={
        'start': 9,
        'end': 15
    })
    assert resp.status_code == 200
    data = resp.get_json()
    assert data['success'] is True
    assert data['doctor']['scheduleHours']['start'] == 9
    assert data['doctor']['scheduleHours']['end'] == 15

    # Test invalid hours
    resp_invalid = client.put(f'/api/admin/schedules/{seed_doctor.id}/hours', json={
        'start': 18,
        'end': 10
    })
    assert resp_invalid.status_code == 400
