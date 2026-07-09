import sys
import os

# Ensure the current directory is in the path
sys.path.insert(0, os.path.dirname(__file__))

from app import create_app
from app.extensions import db
from app.models import Admin, Doctor, Patient
from sqlalchemy import text

app = create_app()

def verify_database():
    with app.app_context():
        print("="*60)
        print(" CLINK Database Verification Script")
        print("="*60)
        
        try:
            # Check connection and database engine
            result = db.session.execute(text("SELECT version();")).fetchone()
            print(f"\n[OK] Successfully connected to the database!")
            print(f"[INFO] Database Version: \n   {result[0].split(',')[0]}")
            
            # Fetch counts from the tables
            admin_count = Admin.query.count()
            doctor_count = Doctor.query.count()
            patient_count = Patient.query.count()
            
            print("\n--- Database Statistics ---")
            print(f"   - Admins:   {admin_count}")
            print(f"   - Doctors:  {doctor_count}")
            print(f"   - Patients: {patient_count}")
            
            print("\n--- Sample Doctors Fetched ---")
            for doc in Doctor.query.limit(3).all():
                print(f"   - {doc.name} (Specialization: {doc.specialization})")
                
            print("\n--- Sample Patients Fetched ---")
            for pat in Patient.query.limit(3).all():
                print(f"   - {pat.name} (Email: {pat.email})")
                
            print("\n[SUCCESS] Database integration is verified and fully working!")
            print("="*60)
            
        except Exception as e:
            print("\n❌ Failed to connect to the database!")
            print(f"Error details: {e}")

if __name__ == "__main__":
    verify_database()
