"""
CLINK — Auth Controller
Handles registration, login, and logout routes.
"""
from functools import wraps
import secrets
from datetime import datetime, timedelta
from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash, session
from flask_login import login_user, logout_user, login_required, current_user
from app.services.auth_service import AuthService
from app.extensions import db

auth_bp = Blueprint('auth', __name__)

RESET_TOKENS = {}



def role_required(*roles):
    """Decorator to restrict access based on user role (NFR-019)."""
    def decorator(f):
        @wraps(f)
        @login_required
        def decorated_function(*args, **kwargs):
            user_role = getattr(current_user, 'role', None)
            if user_role not in roles:
                flash('You do not have permission to access this page.', 'error')
                return redirect(url_for('auth.login_page'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator


# --- Page Routes ---

@auth_bp.route('/login', methods=['GET'])
def login_page():
    if current_user.is_authenticated:
        return _redirect_by_role(current_user.role)
    return render_template('auth/login.html')


@auth_bp.route('/register', methods=['GET'])
def register_page():
    if current_user.is_authenticated:
        return _redirect_by_role(current_user.role)
    return render_template('auth/register.html')


@auth_bp.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password_page():
    if current_user.is_authenticated:
        return _redirect_by_role(current_user.role)
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        if not email:
            flash('Email address is required.', 'error')
            return render_template('auth/forgot_password.html')
            
        from app.models.patient import Patient
        from app.models.doctor import Doctor
        from app.models.admin import Admin
        
        user = None
        role = None
        
        patient = Patient.query.filter_by(email=email).first()
        if patient:
            user = patient
            role = 'patient'
        else:
            doctor = Doctor.query.filter_by(email=email).first()
            if doctor:
                user = doctor
                role = 'doctor'
            else:
                admin = Admin.query.filter_by(email=email).first()
                if admin:
                    user = admin
                    role = 'admin'
                    
        if user:
            token = secrets.token_urlsafe(32)
            expiry = datetime.utcnow() + timedelta(hours=1)
            RESET_TOKENS[token] = {
                'email': email,
                'role': role,
                'expiry': expiry
            }
            reset_url = url_for('auth.reset_password', token=token, _external=True)
            flash(f"Password reset link (simulated): {reset_url}", 'success')
        else:
            # For security, keep standard message, but as per guidelines let's flash it if exists
            flash('If the email exists, a password reset link has been generated.', 'info')
            
        return redirect(url_for('auth.login_page'))
        
    return render_template('auth/forgot_password.html')


@auth_bp.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return _redirect_by_role(current_user.role)
        
    token_data = RESET_TOKENS.get(token)
    if not token_data or token_data['expiry'] < datetime.utcnow():
        if token in RESET_TOKENS:
            del RESET_TOKENS[token]
        flash('Invalid or expired password reset token.', 'error')
        return redirect(url_for('auth.login_page'))
        
    if request.method == 'POST':
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        if not password or password != confirm_password:
            flash('Passwords do not match.', 'error')
            return render_template('auth/reset_password.html', token=token)
            
        valid, err = AuthService.validate_password(password)
        if not valid:
            flash(err, 'error')
            return render_template('auth/reset_password.html', token=token)
            
        email = token_data['email']
        role = token_data['role']
        
        from app.models.patient import Patient
        from app.models.doctor import Doctor
        from app.models.admin import Admin
        
        if role == 'patient':
            user = Patient.query.filter_by(email=email).first()
        elif role == 'doctor':
            user = Doctor.query.filter_by(email=email).first()
        else:
            user = Admin.query.filter_by(email=email).first()
            
        if user:
            user.password = AuthService.hash_password(password)
            db.session.commit()
            del RESET_TOKENS[token]
            flash('Your password has been reset successfully. Please log in.', 'success')
            return redirect(url_for('auth.login_page'))
        else:
            flash('User not found.', 'error')
            return redirect(url_for('auth.login_page'))
            
    return render_template('auth/reset_password.html', token=token)



# --- API Routes ---

@auth_bp.route('/api/auth/register', methods=['POST'])
def register():
    """UC001: Patient Registration."""
    data = request.get_json()
    if not data:
        return jsonify({'success': False, 'error': 'Invalid request data.'}), 400

    patient, error = AuthService.register_patient(
        name=data.get('name', ''),
        email=data.get('email', ''),
        phone=data.get('phone', ''),
        password=data.get('password', ''),
        gender=data.get('gender', ''),
        dob=data.get('dob', ''),
    )

    if error:
        return jsonify({'success': False, 'error': error}), 400

    # Auto-login after registration
    login_user(patient)
    return jsonify({
        'success': True,
        'message': 'Registration successful!',
        'redirect': url_for('patient.dashboard')
    })


@auth_bp.route('/api/auth/login', methods=['POST'])
def login():
    """Login for all roles."""
    data = request.get_json()
    if not data:
        return jsonify({'success': False, 'error': 'Invalid request data.'}), 400

    user, role, error = AuthService.authenticate(
        email=data.get('email', ''),
        password=data.get('password', ''),
    )

    if error:
        return jsonify({'success': False, 'error': error}), 401

    login_user(user)
    redirect_url = _redirect_url_by_role(role)
    return jsonify({
        'success': True,
        'message': f'Welcome back, {user.name}!',
        'role': role,
        'redirect': redirect_url
    })


@auth_bp.route('/api/auth/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({'success': True, 'redirect': url_for('auth.login_page')})


@auth_bp.route('/logout')
@login_required
def logout_page():
    logout_user()
    return redirect(url_for('auth.login_page'))


# --- Helpers ---

def _redirect_by_role(role):
    if role == 'doctor':
        return redirect(url_for('doctor.dashboard'))
    elif role == 'admin':
        return redirect(url_for('admin.dashboard'))
    return redirect(url_for('patient.dashboard'))


def _redirect_url_by_role(role):
    if role == 'doctor':
        return url_for('doctor.dashboard')
    elif role == 'admin':
        return url_for('admin.dashboard')
    return url_for('patient.dashboard')
