"""
CLINK — AI Triage Service
Handles symptom analysis, urgency classification, and specialist recommendation.
Uses scikit-learn Decision Tree classifier.
"""
import os
import joblib
import numpy as np
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import LabelEncoder
import re

# Disease → specialist mapping
SPECIALIST_MAP = {
    'Fungal infection': 'Dermatologist',
    'Allergy': 'Allergist',
    'GERD': 'Gastroenterologist',
    'Chronic cholestasis': 'Hepatologist',
    'Drug Reaction': 'Allergist',
    'Peptic ulcer diseae': 'Gastroenterologist',
    'AIDS': 'Infectious Disease Specialist',
    'Diabetes': 'Endocrinologist',
    'Gastroenteritis': 'Gastroenterologist',
    'Bronchial Asthma': 'Pulmonologist',
    'Hypertension': 'Cardiologist',
    'Migraine': 'Neurologist',
    'Cervical spondylosis': 'Orthopedic Surgeon',
    'Paralysis (brain hemorrhage)': 'Neurologist',
    'Jaundice': 'Hepatologist',
    'Malaria': 'Infectious Disease Specialist',
    'Chicken pox': 'Infectious Disease Specialist',
    'Dengue': 'Infectious Disease Specialist',
    'Typhoid': 'Infectious Disease Specialist',
    'hepatitis A': 'Hepatologist',
    'Hepatitis B': 'Hepatologist',
    'Hepatitis C': 'Hepatologist',
    'Hepatitis D': 'Hepatologist',
    'Hepatitis E': 'Hepatologist',
    'Alcoholic hepatitis': 'Hepatologist',
    'Tuberculosis': 'Pulmonologist',
    'Common Cold': 'General Practitioner',
    'Pneumonia': 'Pulmonologist',
    'Dimorphic hemmorhoids(piles)': 'General Surgeon',
    'Heart attack': 'Cardiologist',
    'Varicose veins': 'Vascular Surgeon',
    'Hypothyroidism': 'Endocrinologist',
    'Hyperthyroidism': 'Endocrinologist',
    'Hypoglycemia': 'Endocrinologist',
    'Osteoarthristis': 'Rheumatologist',
    'Arthritis': 'Rheumatologist',
    '(vertigo) Paroxymal  Positional Vertigo': 'ENT Specialist',
    'Acne': 'Dermatologist',
    'Urinary tract infection': 'Urologist',
    'Psoriasis': 'Dermatologist',
    'Impetigo': 'Dermatologist',
}

class AITriageService:
    """AI-based symptom analysis using Decision Tree classifier."""

    _model = None
    _label_encoder = None
    _model_dir = os.path.join(os.path.dirname(__file__), '..', 'ai')

    @classmethod
    def _get_model_path(cls):
        return os.path.join(cls._model_dir, 'model.pkl')

    @classmethod
    def _get_encoder_path(cls):
        return os.path.join(cls._model_dir, 'label_encoder.pkl')

    @classmethod
    def train_model(cls):
        """
        Train the Decision Tree model on the symptom dataset and parse additional metadata.
        """
        from sklearn.model_selection import train_test_split
        
        data2_dir = os.path.join(cls._model_dir, 'data2')
        dataset_path = os.path.join(data2_dir, 'dataset.csv')
        desc_path = os.path.join(data2_dir, 'symptom_Description.csv')
        prec_path = os.path.join(data2_dir, 'symptom_precaution.csv')
        sev_path = os.path.join(data2_dir, 'Symptom-severity.csv')

        if not os.path.exists(dataset_path):
            print(f"[AI] Error: Dataset not found at {dataset_path}")
            return None, None

        # 1. Train Model
        df = pd.read_csv(dataset_path)
        
        symptoms_set = set()
        for col in df.columns[1:]:
            unique_vals = df[col].dropna().unique()
            for val in unique_vals:
                val_str = str(val).strip()
                if val_str and val_str.lower() != 'nan':
                    clean_symp = re.sub(r'\s+', '_', val_str.lower())
                    symptoms_set.add(clean_symp)
        symptom_cols = sorted(list(symptoms_set))
        
        encoded_data = []
        for idx, row in df.iterrows():
            row_symptoms = []
            for val in row[1:].dropna():
                val_str = str(val).strip()
                if val_str and val_str.lower() != 'nan':
                    row_symptoms.append(re.sub(r'\s+', '_', val_str.lower()))
            
            encoded_row = {s: 1 if s in row_symptoms else 0 for s in symptom_cols}
            encoded_row['prognosis'] = str(row['Disease']).strip()
            encoded_data.append(encoded_row)
        
        processed_df = pd.DataFrame(encoded_data)

        X = processed_df[symptom_cols].values
        y = processed_df['prognosis'].values

        le = LabelEncoder()
        y_encoded = le.fit_transform(y)

        X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.2, random_state=42)

        model = DecisionTreeClassifier(random_state=42)
        model.fit(X_train, y_train)
        
        accuracy = model.score(X_test, y_test)

        os.makedirs(cls._model_dir, exist_ok=True)
        joblib.dump(model, cls._get_model_path())
        joblib.dump(le, cls._get_encoder_path())
        joblib.dump(symptom_cols, os.path.join(cls._model_dir, 'feature_names.pkl'))

        # 2. Parse Descriptions
        descriptions = {}
        if os.path.exists(desc_path):
            desc_df = pd.read_csv(desc_path)
            for _, row in desc_df.iterrows():
                disease = str(row['Disease']).strip()
                desc = str(row['Description']).strip()
                descriptions[disease] = desc
        joblib.dump(descriptions, os.path.join(cls._model_dir, 'descriptions.pkl'))

        # 3. Parse Precautions
        precautions = {}
        if os.path.exists(prec_path):
            prec_df = pd.read_csv(prec_path)
            for _, row in prec_df.iterrows():
                disease = str(row['Disease']).strip()
                precs = [str(p).strip().capitalize() for p in row[1:].dropna() if str(p).strip()]
                precautions[disease] = precs
        joblib.dump(precautions, os.path.join(cls._model_dir, 'precautions.pkl'))

        # 4. Parse Severities
        severities = {}
        if os.path.exists(sev_path):
            sev_df = pd.read_csv(sev_path)
            for _, row in sev_df.iterrows():
                symp = str(row['Symptom']).strip()
                clean_symp = re.sub(r'\s+', '_', symp.lower())
                weight = row['weight']
                try:
                    severities[clean_symp] = int(weight)
                except ValueError:
                    pass
        joblib.dump(severities, os.path.join(cls._model_dir, 'severities.pkl'))

        cls._model = model
        cls._label_encoder = le
        print(f"[AI] Model trained. Classes: {len(le.classes_)}, Features: {len(symptom_cols)}, Validation Accuracy: {accuracy:.4f}")
        return model, le

    @classmethod
    def evaluate_model(cls):
        """
        Measure model accuracy on demand, from scratch, every call.

        Reports two figures:
        - Held-out 20% test split accuracy/precision/recall/F1 (same split
          method used to produce the persisted model.pkl).
        - Stratified 5-fold cross-validation accuracy (mean +/- std) — the
          model is retrained and tested 5 times on different splits, so no
          single "lucky" split can inflate the score. This is the number
          that should be quoted as "the" accuracy.

        Does not touch or overwrite the persisted model.pkl.
        """
        from sklearn.model_selection import train_test_split, StratifiedKFold, cross_val_score
        from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

        data2_dir = os.path.join(cls._model_dir, 'data2')
        dataset_path = os.path.join(data2_dir, 'dataset.csv')
        if not os.path.exists(dataset_path):
            return None

        df = pd.read_csv(dataset_path)

        symptoms_set = set()
        for col in df.columns[1:]:
            for val in df[col].dropna().unique():
                val_str = str(val).strip()
                if val_str and val_str.lower() != 'nan':
                    symptoms_set.add(re.sub(r'\s+', '_', val_str.lower()))
        symptom_cols = sorted(symptoms_set)

        encoded_data = []
        for _, row in df.iterrows():
            row_symptoms = []
            for val in row[1:].dropna():
                val_str = str(val).strip()
                if val_str and val_str.lower() != 'nan':
                    row_symptoms.append(re.sub(r'\s+', '_', val_str.lower()))
            encoded_row = {s: 1 if s in row_symptoms else 0 for s in symptom_cols}
            encoded_row['prognosis'] = str(row['Disease']).strip()
            encoded_data.append(encoded_row)

        processed_df = pd.DataFrame(encoded_data)
        X = processed_df[symptom_cols].values
        y_raw = processed_df['prognosis'].values

        le = LabelEncoder()
        y = le.fit_transform(y_raw)

        # 1. Held-out 20% test split
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        holdout_model = DecisionTreeClassifier(random_state=42)
        holdout_model.fit(X_train, y_train)
        y_pred = holdout_model.predict(X_test)

        holdout_accuracy = accuracy_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred, average='weighted', zero_division=0)
        recall = recall_score(y_test, y_pred, average='weighted', zero_division=0)
        f1 = f1_score(y_test, y_pred, average='weighted', zero_division=0)

        # 2. Stratified 5-fold cross-validation (the defensible headline number)
        cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
        cv_scores = cross_val_score(
            DecisionTreeClassifier(random_state=42), X, y, cv=cv, scoring='accuracy'
        )

        return {
            'holdoutAccuracy': round(holdout_accuracy * 100, 2),
            'precision': round(precision * 100, 2),
            'recall': round(recall * 100, 2),
            'f1Score': round(f1 * 100, 2),
            'cvMean': round(cv_scores.mean() * 100, 2),
            'cvStd': round(cv_scores.std() * 100, 2),
            'cvFolds': [round(s * 100, 2) for s in cv_scores.tolist()],
            'sampleCount': len(df),
            'classCount': len(le.classes_),
            'featureCount': len(symptom_cols),
        }

    @classmethod
    def load_model(cls):
        """Load the trained model from disk."""
        model_path = cls._get_model_path()
        encoder_path = cls._get_encoder_path()

        if os.path.exists(model_path) and os.path.exists(encoder_path):
            cls._model = joblib.load(model_path)
            cls._label_encoder = joblib.load(encoder_path)
            return True
        return False

    @classmethod
    def ensure_model(cls):
        """Ensure model is loaded; train if not available."""
        if cls._model is None:
            if not cls.load_model():
                cls.train_model()

    @classmethod
    def predict(cls, symptoms_list):
        """
        Predict urgency, specialist, description, and precautions from a list of symptom names.
        """
        cls.ensure_model()

        # Load metadata
        feature_path = os.path.join(cls._model_dir, 'feature_names.pkl')
        feature_names = joblib.load(feature_path) if os.path.exists(feature_path) else []
        
        sev_path = os.path.join(cls._model_dir, 'severities.pkl')
        severities = joblib.load(sev_path) if os.path.exists(sev_path) else {}

        desc_path = os.path.join(cls._model_dir, 'descriptions.pkl')
        descriptions = joblib.load(desc_path) if os.path.exists(desc_path) else {}

        prec_path = os.path.join(cls._model_dir, 'precautions.pkl')
        precautions = joblib.load(prec_path) if os.path.exists(prec_path) else {}

        # Build feature vector and calculate max severity
        features = np.zeros(len(feature_names))
        max_severity = 0
        
        for symptom in symptoms_list:
            symptom_clean = re.sub(r'\s+', '_', symptom.strip().lower())
            
            if symptom_clean in feature_names:
                idx = feature_names.index(symptom_clean)
                features[idx] = 1
                
            # Track severity for dynamic urgency (use 0 if missing)
            sev = severities.get(symptom_clean, 0)
            if sev > max_severity:
                max_severity = sev

        # Predict
        prediction = cls._model.predict([features])[0]
        disease = cls._label_encoder.inverse_transform([prediction])[0]

        # Calculate urgency based on max severity weight (e.g. >= 6 is urgent)
        urgency = 'urgent' if max_severity >= 6 else 'non-urgent'
        
        # Fallback to general practitioner if no specialist maps
        specialist = SPECIALIST_MAP.get(disease, 'General Practitioner')
        desc = descriptions.get(disease, 'No description available.')
        precs = precautions.get(disease, [])

        return {
            'urgencyLevel': urgency,
            'recommendedSpecialist': specialist,
            'predictedCondition': disease,
            'description': desc,
            'precautions': precs
        }

    @classmethod
    def get_symptom_list(cls):
        """Return the list of supported symptoms for the UI."""
        return [s.replace('_', ' ').title() for s in cls.get_symptom_codes()]

    @classmethod
    def get_symptom_codes(cls):
        """Return raw symptom codes."""
        feature_path = os.path.join(cls._model_dir, 'feature_names.pkl')
        if os.path.exists(feature_path):
            return joblib.load(feature_path)
        return []
