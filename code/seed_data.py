"""
CLINK — Database Seeding Script
Pre-populates the database with admin, sample doctors, and sample patients.
Run: python seed_data.py
"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from app import create_app
from app.extensions import db
from app.models import Admin, Patient, Doctor
from app.services.auth_service import AuthService

app = create_app()

DOCTORS = [
    {'name': 'Ahmad Al Rashid', 'email': 'dr.ahmad@clink.com', 'specialization': 'General Practitioner'},
    {'name': 'Fatima Al Sabah', 'email': 'dr.fatima@clink.com', 'specialization': 'Cardiologist'},
    {'name': 'Omar Hassan', 'email': 'dr.omar@clink.com', 'specialization': 'Neurologist'},
    {'name': 'Maryam Al Ali', 'email': 'dr.maryam@clink.com', 'specialization': 'Dermatologist'},
    {'name': 'Khalid Nasser', 'email': 'dr.khalid@clink.com', 'specialization': 'Gastroenterologist'},
    {'name': 'Sara Al Mutairi', 'email': 'dr.sara@clink.com', 'specialization': 'Pulmonologist'},
    {'name': 'Youssef Ibrahim', 'email': 'dr.youssef@clink.com', 'specialization': 'Endocrinologist'},
    {'name': 'Layla Al Enezi', 'email': 'dr.layla@clink.com', 'specialization': 'Infectious Disease Specialist'},
    {'name': 'Nadia Al Kandari', 'email': 'dr.nadia@clink.com', 'specialization': 'Rheumatologist'},
    {'name': 'Hassan Al Dosari', 'email': 'dr.hassan@clink.com', 'specialization': 'Hepatologist'},
    {'name': 'Reem Al Fahad', 'email': 'dr.reem@clink.com', 'specialization': 'Orthopedic Surgeon'},
    {'name': 'Ali Al Shammari', 'email': 'dr.ali@clink.com', 'specialization': 'ENT Specialist'},
    {'name': 'Huda Al Ajmi', 'email': 'dr.huda@clink.com', 'specialization': 'Urologist'},
    {'name': 'Tariq Al Harbi', 'email': 'dr.tariq@clink.com', 'specialization': 'Allergist'},
    {'name': 'Salma Al Otaibi', 'email': 'dr.salma@clink.com', 'specialization': 'Vascular Surgeon'},
    {'name': 'Majid Al Subaie', 'email': 'dr.majid@clink.com', 'specialization': 'General Surgeon'},
]

SAMPLE_PATIENTS = [
    {'name': 'Aisha Mohammed', 'email': 'aisha@example.com', 'phone': '96512345678', 'gender': 'Female', 'dob': '1990-03-15'},
    {'name': 'Abdullah Al Faraj', 'email': 'abdullah@example.com', 'phone': '96523456789', 'gender': 'Male', 'dob': '1955-08-22'},
    {'name': 'Noura Al Salem', 'email': 'noura@example.com', 'phone': '96534567890', 'gender': 'Female', 'dob': '1972-11-05'},
]

DEFAULT_PASSWORD = 'Test@123'


def seed():
    with app.app_context():
        print("[SEED] Seeding CLINK database...\n")

        # --- Admin ---
        if not Admin.query.filter_by(email='admin@clink.com').first():
            admin = Admin(
                name='System Admin',
                email='admin@clink.com',
                password=AuthService.hash_password(DEFAULT_PASSWORD),
                role='admin',
                access_level='full',
            )
            db.session.add(admin)
            print("[OK] Admin created: admin@clink.com")
        else:
            print("[SKIP] Admin already exists")

        # --- Doctors ---
        for doc in DOCTORS:
            if not Doctor.query.filter_by(email=doc['email']).first():
                doctor = Doctor(
                    name=doc['name'],
                    email=doc['email'],
                    password=AuthService.hash_password(DEFAULT_PASSWORD),
                    specialization=doc['specialization'],
                    availability='available',
                )
                db.session.add(doctor)
                print(f"[OK] Doctor created: {doc['name']} ({doc['specialization']})")
            else:
                print(f"[SKIP] Doctor already exists: {doc['email']}")

        # --- Sample Patients ---
        for pat in SAMPLE_PATIENTS:
            if not Patient.query.filter_by(email=pat['email']).first():
                from datetime import datetime
                patient = Patient(
                    name=pat['name'],
                    email=pat['email'],
                    phone=pat['phone'],
                    password=AuthService.hash_password(DEFAULT_PASSWORD),
                    gender=pat.get('gender'),
                    dob=datetime.strptime(pat['dob'], '%Y-%m-%d').date() if pat.get('dob') else None,
                )
                db.session.add(patient)
                print(f"[OK] Patient created: {pat['name']} (Gender: {pat.get('gender')}, DoB: {pat.get('dob')})")
            else:
                print(f"[SKIP] Patient already exists: {pat['email']}")

        db.session.commit()
        print(f"\n[DONE] Seeding complete!")
        print(f"\nLogin credentials (all accounts):")
        print(f"   Password: {DEFAULT_PASSWORD}")
        print(f"   Admin:   admin@clink.com")
        print(f"   Doctor:  dr.ahmad@clink.com (or any dr.* email)")
        print(f"   Patient: aisha@example.com (or any sample patient)")


if __name__ == '__main__':
    seed()
