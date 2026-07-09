"""
CLINK — Notification Entity
Stores system notifications sent to users.
"""
from datetime import datetime
from app.extensions import db


class Notification(db.Model):
    __tablename__ = 'notifications'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, nullable=False)
    user_role = db.Column(db.String(10), nullable=False)  # patient / doctor / admin
    message = db.Column(db.String(500), nullable=False)
    notification_type = db.Column(db.String(50), default='info')
    # Types: appointment_confirmed, appointment_updated, case_update, system, info
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    is_read = db.Column(db.Boolean, default=False)
    delivery_status = db.Column(db.String(20), default='sent')  # sent / pending / failed

    def to_dict(self):
        return {
            'id': self.id,
            'userId': self.user_id,
            'userRole': self.user_role,
            'message': self.message,
            'type': self.notification_type,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None,
            'isRead': self.is_read,
            'deliveryStatus': self.delivery_status
        }

    def __repr__(self):
        return f'<Notification {self.id} - {self.user_role}:{self.user_id}>'
