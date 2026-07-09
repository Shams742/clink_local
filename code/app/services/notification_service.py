import requests
import os
import logging
import json
from datetime import datetime
from app.extensions import db
from app.models.notification import Notification

logger = logging.getLogger(__name__)

# Persistent log file inside instance directory
LOG_FILE_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'instance', 'clink_emails.log')

# Initialize simulated email log by reading file
EMAIL_LOG = []
try:
    if os.path.exists(LOG_FILE_PATH):
        with open(LOG_FILE_PATH, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:
                    EMAIL_LOG.append(json.loads(line))
except Exception as e:
    logger.error(f"Error loading EMAIL_LOG from file: {e}")


class NotificationService:
    """Business logic for notification operations."""

    @staticmethod
    def create_notification(user_id, user_role, message, notification_type='info'):
        """
        UC008: Create and store a notification.
        """
        notification = Notification(
            user_id=user_id,
            user_role=user_role,
            message=message,
            notification_type=notification_type,
            delivery_status='sent'
        )
        db.session.add(notification)
        db.session.commit()

        # Simulate email notification (in-memory log for demo)
        NotificationService.simulate_email(
            to=f'{user_role}_{user_id}@clinic.example',
            subject=f'[CLINK] {notification_type.replace("_", " ").title()}',
            body=message,
            notification_id=notification.id
        )

        return notification

    @staticmethod
    def simulate_email(to, subject, body, notification_id=None):
        """Simulate sending an email by logging it to memory and persistent file log."""
        entry = {
            'id': len(EMAIL_LOG) + 1,
            'to': to,
            'subject': subject,
            'body': body,
            'notification_id': notification_id,
            'sent_at': datetime.utcnow().isoformat(),
        }
        EMAIL_LOG.append(entry)

        try:
            os.makedirs(os.path.dirname(LOG_FILE_PATH), exist_ok=True)
            with open(LOG_FILE_PATH, 'a', encoding='utf-8') as f:
                f.write(json.dumps(entry) + '\n')
        except Exception as e:
            logger.error(f"Error saving simulated email to file: {e}")

        logger.info(f'[EMAIL SIMULATION] To: {to} | Subject: {subject}')
        return entry



    @staticmethod
    def get_user_notifications(user_id, user_role, unread_only=False):
        """Get notifications for a specific user."""
        query = Notification.query.filter_by(
            user_id=user_id,
            user_role=user_role
        )
        if unread_only:
            query = query.filter_by(is_read=False)

        return query.order_by(Notification.timestamp.desc()).all()

    @staticmethod
    def get_unread_count(user_id, user_role):
        """Get count of unread notifications."""
        return Notification.query.filter_by(
            user_id=user_id,
            user_role=user_role,
            is_read=False
        ).count()

    @staticmethod
    def mark_as_read(notification_id, user_id, user_role):
        """Mark a notification as read."""
        notification = Notification.query.filter_by(
            id=notification_id,
            user_id=user_id,
            user_role=user_role
        ).first()

        if not notification:
            return None, 'Notification not found.'

        notification.is_read = True
        db.session.commit()
        return notification, None

    @staticmethod
    def mark_all_read(user_id, user_role):
        """Mark all notifications as read for a user."""
        Notification.query.filter_by(
            user_id=user_id,
            user_role=user_role,
            is_read=False
        ).update({'is_read': True})
        db.session.commit()
