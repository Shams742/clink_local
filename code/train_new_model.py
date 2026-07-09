import sys
import os

# Ensure the correct path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from app.services.ai_triage_service import AITriageService

if __name__ == '__main__':
    print("Starting training process...")
    model, le = AITriageService.train_model()
    
    # Verify symptoms were loaded correctly
    symptoms = AITriageService.get_symptom_list()
    print(f"Loaded {len(symptoms)} symptoms dynamically.")
    print("First 10 symptoms:", symptoms[:10])
    
    # Test a prediction
    print("Testing a prediction...")
    result = AITriageService.predict(['itching', 'skin_rash', 'nodal_skin_eruptions'])
    print("Prediction result:", result)
    print("Success!")
