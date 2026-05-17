# # marketing/views.py
# import os
# import joblib
# import pandas as pd
# from django.shortcuts import render
# from django.conf import settings
# from .forms import MarketingPredictionForm

# # 1. Define paths to your models (Update these filenames if yours are different!)
# MODEL_DIR = os.path.join(settings.BASE_DIR, 'marketing', 'ml_models')
# MODEL_PATH = os.path.join(MODEL_DIR, 'best_marketing_campaign_pipeline.pkl')
# SCALER_PATH = os.path.join(MODEL_DIR, 'marketing_scaler.pkl')
# FEATURES_PATH = os.path.join(MODEL_DIR, 'selected_marketing_features.pkl')

# svm_model = None
# scaler = None
# expected_features = None

# # 2. Load models globally
# try:
#     svm_model = joblib.load(MODEL_PATH)
#     scaler = joblib.load(SCALER_PATH)
#     expected_features = joblib.load(FEATURES_PATH)
#     print("SUCCESS: ML Models loaded perfectly!")
# except FileNotFoundError as e:
#     print(f"CRITICAL WARNING: ML files missing. {e}")

# def predict_view(request):
#     error_message = None

#     if request.method == 'POST':
#         form = MarketingPredictionForm(request.POST)
#         if form.is_valid():
#             if expected_features is None or scaler is None or svm_model is None:
#                 error_message = "Server Error: ML models missing."
#             else:
#                 form_data = form.cleaned_data
#                 input_df = pd.DataFrame([form_data])
                
#                 try:
#                     # 1. Ask the scaler exactly what columns it needs (e.g., all 31)
#                     scaler_features = getattr(scaler, 'feature_names_in_', expected_features)
                    
#                     # 2. Automatically fill any missing columns (like AcceptedCmp1) with 0
#                     for col in scaler_features:
#                         if col not in input_df.columns:
#                             input_df[col] = 0
                            
#                     # 3. Order the dataframe exactly how the scaler expects it
#                     input_df = input_df[scaler_features]
                    
#                     # 4. Scale the data safely
#                     scaled_array = scaler.transform(input_df)
                    
#                     # 5. Convert back to DataFrame
#                     scaled_df = pd.DataFrame(scaled_array, columns=scaler_features)
                    
#                     # 6. Slice ONLY the exact 15 features the final SVM model expects
#                     final_input_df = scaled_df[expected_features]
                    
#                     # 7. Predict using the SVM
#                     prediction = svm_model.predict(final_input_df)
                    
#                     if prediction[0] == 1:
#                         prediction_result = "Success: High probability of response."
#                     else:
#                         prediction_result = "Failure: Low probability of response."
                        
#                     # Route to the Result Page
#                     context = {
#                         'prediction_result': prediction_result,
#                         'input_data': form_data
#                     }
#                     return render(request, 'marketing/result.html', context)

#                 except Exception as e:
#                     error_message = f"Processing Error: {str(e)}"
#     else:
#         form = MarketingPredictionForm()

#     return render(request, 'marketing/predict.html', {
#         'form': form,
#         'error_message': error_message
#     })

# with database
# marketing/views.py
import os
import joblib
import pandas as pd
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from .forms import MarketingPredictionForm
from .models import CustomerPrediction

# 1. Define paths to your models (Update these filenames if yours are different!)
MODEL_DIR = os.path.join(settings.BASE_DIR, 'marketing', 'ml_models')
MODEL_PATH = os.path.join(MODEL_DIR, 'best_marketing_campaign_pipeline.pkl')
SCALER_PATH = os.path.join(MODEL_DIR, 'marketing_scaler.pkl')
FEATURES_PATH = os.path.join(MODEL_DIR, 'selected_marketing_features.pkl')

svm_model = None
scaler = None
expected_features = None

try:
    svm_model = joblib.load(MODEL_PATH)
    scaler = joblib.load(SCALER_PATH)
    expected_features = joblib.load(FEATURES_PATH)
except FileNotFoundError as e:
    print(f"WARNING: ML files missing. {e}")

def dashboard_view(request):
    """Shows the table of all saved predictions."""
    predictions = CustomerPrediction.objects.all().order_by('-created_at')
    return render(request, 'marketing/dashboard.html', {'predictions': predictions})

def predict_view(request, pk=None):
    """Handles BOTH adding new predictions and editing existing ones."""
    # If a primary key (pk) is passed, we are editing. Otherwise, creating new.
    record = get_object_or_404(CustomerPrediction, pk=pk) if pk else None
    error_message = None

    if request.method == 'POST':
        form = MarketingPredictionForm(request.POST, instance=record)
        if form.is_valid():
            if expected_features is None or scaler is None or svm_model is None:
                error_message = "Server Error: ML models missing."
            else:
                try:
                    # 1. Save form data temporarily without committing to DB yet
                    instance = form.save(commit=False)
                    
                    # 2. Extract data into DataFrame for the ML model
                    form_data = form.cleaned_data
                    input_df = pd.DataFrame([form_data])
                    
                    # 3. Apply the Pipeline workaround for missing columns
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
                        instance.prediction_result = "Success: High probability of response."
                    else:
                        instance.prediction_result = "Failure: Low probability of response."
                        
                    # 4. Save to Database!
                    instance.save()
                    
                    # 5. Redirect to the result page for this specific record
                    return redirect('result', pk=instance.pk)

                except Exception as e:
                    error_message = f"Processing Error: {str(e)}"
    else:
        # Load form. If 'record' exists, it populates the fields with the saved data!
        form = MarketingPredictionForm(instance=record)

    return render(request, 'marketing/predict.html', {
        'form': form, 
        'error_message': error_message,
        'is_edit': pk is not None
    })

def result_view(request, pk):
    """Shows the final result for a specific prediction."""
    record = get_object_or_404(CustomerPrediction, pk=pk)
    return render(request, 'marketing/result.html', {'record': record})

def delete_view(request, pk):
    """Deletes a record and returns to dashboard."""
    record = get_object_or_404(CustomerPrediction, pk=pk)
    if request.method == 'POST':
        record.delete()
    return redirect('dashboard')