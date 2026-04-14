"""
Prediction engine — builds the feature row, fills hidden defaults,
runs inference, and returns structured results.
"""

import pandas as pd
import numpy as np
from .model_loader import load_model, load_feature_columns, load_reference_data
from .feature_config import get_all_ui_features, FEATURE_DESCRIPTIONS


def build_feature_row(user_inputs: dict) -> pd.DataFrame:
    """
    Build a single-row DataFrame with ALL features in the exact trained order.

    - User-provided values are placed directly.
    - Missing / hidden columns are filled from dataset medians.
    - The final DataFrame column order matches the saved feature_columns exactly.
    """
    feature_cols = load_feature_columns()
    medians = load_reference_data()

    row = {}
    for col in feature_cols:
        if col in user_inputs and user_inputs[col] is not None:
            row[col] = user_inputs[col]
        elif col in medians:
            row[col] = medians[col]
        else:
            # Fallback: use NaN — the pipeline's SimpleImputer will handle it
            row[col] = np.nan

    df = pd.DataFrame([row], columns=feature_cols)
    return df


def predict(user_inputs: dict) -> dict:
    """
    Run full prediction pipeline.

    Returns:
        dict with keys:
            label        : int (1=ASD, 0=Non-ASD)
            label_text   : str ("ASD" | "Non-ASD")
            probability  : float (ASD class probability)
            confidence   : float (confidence for the predicted class)
            feature_row  : pd.DataFrame (the exact row passed to the model)
            hidden_info  : dict mapping hidden col -> (value, source)
    """
    model = load_model()
    feature_cols = load_feature_columns()
    medians = load_reference_data()
    ui_features = get_all_ui_features()

    # Build the row
    feature_row = build_feature_row(user_inputs)

    # Predict
    pred_label = int(model.predict(feature_row)[0])
    pred_proba = model.predict_proba(feature_row)[0]  # [prob_class_0, prob_class_1]

    asd_prob = float(pred_proba[1])
    confidence = float(pred_proba[pred_label])

    # Build hidden features info  (which features were auto-filled)
    hidden_info = {}
    for col in feature_cols:
        if col not in ui_features:
            val = feature_row[col].values[0]
            source = "Dataset median" if col in medians else "NaN (imputed by pipeline)"
            desc = FEATURE_DESCRIPTIONS.get(col, col)
            hidden_info[col] = {
                "value": val,
                "source": source,
                "description": desc,
            }

    return {
        "label": pred_label,
        "label_text": "ASD" if pred_label == 1 else "Non-ASD",
        "probability": asd_prob,
        "confidence": confidence,
        "feature_row": feature_row,
        "hidden_info": hidden_info,
    }


def generate_interpretation(result: dict) -> str:
    """Generate a human-readable interpretation paragraph."""
    label = result["label_text"]
    conf = result["confidence"] * 100
    prob = result["probability"] * 100

    if label == "ASD":
        return (
            f"Based on the clinical, behavioral, and assessment inputs provided, "
            f"the model predicts **ASD (Autism Spectrum Disorder)** with a confidence "
            f"of **{conf:.1f}%** (ASD probability: {prob:.1f}%). "
            f"The combination of ADOS scores, ADI-R interview data, cognitive measures, "
            f"and demographic information contributed to this prediction. "
            f"This result suggests patterns consistent with autism spectrum presentations "
            f"observed in the training dataset."
        )
    else:
        return (
            f"Based on the clinical, behavioral, and assessment inputs provided, "
            f"the model predicts **Non-ASD (Typical Development)** with a confidence "
            f"of **{conf:.1f}%** (ASD probability: {prob:.1f}%). "
            f"The input profile does not strongly match the autism spectrum patterns "
            f"observed in the training dataset. However, a formal clinical evaluation "
            f"is always recommended for conclusive assessment."
        )


def generate_recommendation(result: dict) -> str:
    """Generate a short recommendation note."""
    label = result["label_text"]
    conf = result["confidence"] * 100

    if label == "ASD" and conf > 80:
        return (
            "🔹 **Recommended next step:** Consider a comprehensive clinical evaluation "
            "with a qualified developmental specialist or multidisciplinary team for "
            "formal diagnosis and support planning."
        )
    elif label == "ASD" and conf <= 80:
        return (
            "🔹 **Recommended next step:** The prediction shows moderate confidence. "
            "A thorough clinical assessment by a licensed professional is highly recommended "
            "to clarify the diagnostic picture."
        )
    elif label == "Non-ASD" and conf > 80:
        return (
            "🔹 **Note:** The model does not detect strong ASD indicators in this profile. "
            "If concerns remain, consult a developmental pediatrician or psychologist "
            "for further evaluation."
        )
    else:
        return (
            "🔹 **Note:** The prediction has limited confidence. Clinical judgment should "
            "take precedence. A professional assessment is recommended regardless of "
            "the model's output."
        )
