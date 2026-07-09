"""
CLINK — AI Triage Model Accuracy Report
Run this to independently verify the triage model's accuracy.
Usage: python test_model_accuracy.py
"""
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from app.services.ai_triage_service import AITriageService

if __name__ == '__main__':
    print("Evaluating CLINK AI triage model...\n")
    results = AITriageService.evaluate_model()

    if not results:
        print("Dataset not found — cannot evaluate.")
        sys.exit(1)

    print(f"Dataset: {results['sampleCount']} records | "
          f"{results['classCount']} conditions | "
          f"{results['featureCount']} symptoms\n")

    print("--- Held-out 20% test split ---")
    print(f"Accuracy:  {results['holdoutAccuracy']}%")
    print(f"Precision: {results['precision']}% (weighted)")
    print(f"Recall:    {results['recall']}% (weighted)")
    print(f"F1 Score:  {results['f1Score']}% (weighted)")
    print()

    print("--- Stratified 5-fold cross-validation (the headline number) ---")
    print(f"Mean accuracy: {results['cvMean']}% (+/- {results['cvStd']}%)")
    print(f"Per-fold:      {results['cvFolds']}%")
    print()

    print("Evaluating robustness under incomplete/noisy symptom input...\n")
    robustness = AITriageService.evaluate_robustness()

    if not robustness:
        print("Dataset not found — cannot evaluate robustness.")
        sys.exit(1)

    print(f"Test set: {robustness['testSetSize']} cases | "
          f"{robustness['trialsPerLevel']} trials per corruption level\n")
    print(f"{'Symptoms Dropped':<20}{'Condition Accuracy':<22}{'Urgency Accuracy':<20}")
    for level in robustness['levels']:
        label = f"{level['symptomsDropped']}" + (" (clean)" if level['symptomsDropped'] == 0 else "")
        print(f"{label:<20}{str(level['diseaseAccuracy']) + '%':<22}{str(level['urgencyAccuracy']) + '%':<20}")
