"""
CLINK — Admin Entity
Stores administrative user details and system roles.
"""
from flask_login import UserMixin
from app.extensions import db


class Admin(UserMixin, db.Model):
    __tablename__ = 'admins'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(10), default='admin')
    access_level = db.Column(db.String(50), default='full')  # full / limited

    def get_id(self):
        return f"admin-{self.id}"

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'role': self.role,
            'accessLevel': self.access_level
        }

    def __repr__(self):
        return f'<Admin {self.name}>'
