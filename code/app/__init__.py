"""
CLINK — Smart Outpatient Triage and Scheduling System
Flask Application Factory
"""
import os
from flask import Flask, redirect, url_for
from app.config import config
from app.extensions import db, login_manager, migrate


def create_app(config_name=None):
    """Create and configure the Flask application."""
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'development')

    app = Flask(
        __name__,
        template_folder=os.path.join(os.path.dirname(os.path.dirname(__file__)), 'templates'),
        static_folder=os.path.join(os.path.dirname(__file__), 'static'),
    )
    app.config.from_object(config.get(config_name, config['default']))

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)

    # User loader for Flask-Login
    @login_manager.user_loader
    def load_user(user_id):
        from app.services.auth_service import AuthService
        return AuthService.get_user_by_id(user_id)

    # Register blueprints
    from app.controllers.auth_controller import auth_bp
    from app.controllers.patient_controller import patient_bp
    from app.controllers.doctor_controller import doctor_bp
    from app.controllers.appointment_controller import appointment_bp
    from app.controllers.admin_controller import admin_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(patient_bp)
    app.register_blueprint(appointment_bp)
    app.register_blueprint(doctor_bp)
    app.register_blueprint(admin_bp)

    # Jinja2 custom filter: parse JSON strings in templates
    import json as _json
    @app.template_filter('from_json')
    def from_json_filter(value):
        try:
            return _json.loads(value)
        except Exception:
            return {}

    # Context processor: inject unread notification count for all logged-in users
    @app.context_processor
    def inject_unread_count():
        from flask_login import current_user
        if current_user.is_authenticated:
            from app.services.notification_service import NotificationService
            role = getattr(current_user, 'role', 'patient')
            count = NotificationService.get_unread_count(current_user.id, role)
            return {'global_unread_count': count}
        return {'global_unread_count': 0}

    # Root route
    @app.route('/')
    def index():
        from flask_login import current_user
        if current_user.is_authenticated:
            role = getattr(current_user, 'role', 'patient')
            if role == 'doctor':
                return redirect(url_for('doctor.dashboard'))
            elif role == 'admin':
                return redirect(url_for('admin.dashboard'))
            return redirect(url_for('patient.dashboard'))
        return redirect(url_for('auth.login_page'))

    # Error handlers
    @app.errorhandler(404)
    def not_found(e):
        from flask import render_template
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def server_error(e):
        from flask import render_template
        return render_template('errors/500.html'), 500

    # Create tables and ensure model on first run
    with app.app_context():
        try:
            from app.models import Admin, Patient, Doctor, SymptomRecord, Appointment, Notification, AuditLog
            db.create_all()
            
            # Train AI model if not already trained
            from app.services.ai_triage_service import AITriageService
            AITriageService.ensure_model()
        except Exception as e:
            print(f"Startup initialization skipped or failed (expected on Vercel): {e}")

    return app
