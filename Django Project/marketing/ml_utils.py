import os
import joblib
import pandas as pd
from django.conf import settings

MODEL_DIR = os.path.join(settings.BASE_DIR, 'marketing', 'ml_models')
MODEL_PATH = os.path.join(MODEL_DIR, 'best_marketing_campaign_pipeline.pkl')
SCALER_PATH = os.path.join(MODEL_DIR, 'marketing_scaler.pkl')
FEATURES_PATH = os.path.join(MODEL_DIR, 'selected_marketing_features.pkl')

_cached_models = None


def load_prediction_models():
    global _cached_models
    if _cached_models is not None:
        return _cached_models

    try:
        svm_model = joblib.load(MODEL_PATH)
        scaler = joblib.load(SCALER_PATH)
        expected_features = joblib.load(FEATURES_PATH)
        _cached_models = (scaler, expected_features, svm_model)
        return _cached_models
    except FileNotFoundError as exc:
        raise RuntimeError(
            f"Prediction model files not found. Ensure the ml_models directory contains {MODEL_PATH}, {SCALER_PATH}, and {FEATURES_PATH}."
        ) from exc


def predict_result(form_data: dict) -> str:
    scaler, expected_features, svm_model = load_prediction_models()

    input_df = pd.DataFrame([form_data])
    scaler_features = getattr(scaler, 'feature_names_in_', expected_features)

    for col in scaler_features:
        if col not in input_df.columns:
            input_df[col] = 0

    input_df = input_df[scaler_features]
    scaled_array = scaler.transform(input_df)
    scaled_df = pd.DataFrame(scaled_array, columns=scaler_features)
    final_input_df = scaled_df[expected_features]
    prediction = svm_model.predict(final_input_df)

    if prediction[0] == 1:
        return "Success: High probability of response."
    return "Failure: Low probability of response."
