"""
CLINK — Audit Log Entity
Stores admin action audit trail for accountability and compliance.
"""
from datetime import datetime
from app.extensions import db


class AuditLog(db.Model):
    __tablename__ = 'audit_logs'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    admin_id = db.Column(db.Integer, nullable=False)
    action = db.Column(db.String(100), nullable=False)  # e.g. 'create_doctor', 'deactivate_user'
    target_type = db.Column(db.String(50), nullable=True)  # 'doctor', 'patient', 'appointment'
    target_id = db.Column(db.Integer, nullable=True)
    details = db.Column(db.String(500), nullable=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'adminId': self.admin_id,
            'action': self.action,
            'targetType': self.target_type,
            'targetId': self.target_id,
            'details': self.details,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None,
        }

    def __repr__(self):
        return f'<AuditLog {self.id}: {self.action}>'
