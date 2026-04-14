"""
Model & resource loading utilities.
Loads the pretrained model and feature columns from disk with Streamlit caching.

Fixes applied:
- Added proper error messages that surface in UI
- TTL on cache_data so reference data refreshes if file changes
- Defensive NaN handling
- Cross-sklearn-version SimpleImputer compatibility shim (_fill_dtype patch)
"""

import os
import joblib
import pandas as pd
import numpy as np
import streamlit as st

# ── Compatibility shim 1: ColumnTransformer _RemainderColsList ────────────────
try:
    from sklearn.compose import _column_transformer as _ct
except ImportError:
    _ct = None

if _ct is not None and not hasattr(_ct, "_RemainderColsList"):
    class _RemainderColsList(list):
        pass
    _ct._RemainderColsList = _RemainderColsList


# ── Compatibility shim 2: SimpleImputer _fill_dtype ──────────────────────────
def _patch_sklearn_objects(obj, _visited=None):
    """
    Recursively walk a (possibly nested) sklearn object and patch any
    SimpleImputer that is missing `_fill_dtype`.

    This fixes the cross-version error:
        'SimpleImputer' object has no attribute '_fill_dtype'
    which occurs when a model pickled with sklearn 1.4+ is loaded by
    sklearn < 1.4, or vice-versa.
    """
    if _visited is None:
        _visited = set()
    obj_id = id(obj)
    if obj_id in _visited:
        return
    _visited.add(obj_id)

    try:
        from sklearn.impute import SimpleImputer
        if isinstance(obj, SimpleImputer):
            if not hasattr(obj, '_fill_dtype'):
                obj._fill_dtype = np.float64
            if not hasattr(obj, 'feature_names_in_'):
                pass  # only set if fitted; don't force-set
    except ImportError:
        pass

    # Recurse through common sklearn containers
    for attr in ("steps", "transformers", "transformers_"):
        container = getattr(obj, attr, None)
        if container is None:
            continue
        for item in container:
            # item may be (name, estimator) or (name, estimator, cols)
            sub = item[1] if isinstance(item, (tuple, list)) and len(item) >= 2 else item
            _patch_sklearn_objects(sub, _visited)

    for attr in ("named_steps", "named_transformers_"):
        mapping = getattr(obj, attr, None)
        if isinstance(mapping, dict):
            for sub in mapping.values():
                _patch_sklearn_objects(sub, _visited)

    estimator = getattr(obj, "estimator", None) or getattr(obj, "base_estimator", None)
    if estimator is not None:
        _patch_sklearn_objects(estimator, _visited)

# ── Paths ────────────────────────────────────────────────────────────────────
BASE_DIR      = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH    = os.path.join(BASE_DIR, "models", "asd_ucla_best_model.joblib")
FEATURES_PATH = os.path.join(BASE_DIR, "models", "asd_ucla_feature_columns.joblib")
DATA_PATH     = os.path.join(BASE_DIR, "data",   "UCLA_Master_Features-1-1-5.csv")


@st.cache_resource(show_spinner=False)
def load_model():
    """Load the pretrained sklearn pipeline (LogisticRegression) from joblib."""
    if not os.path.exists(MODEL_PATH):
        st.error(
            f"⚠️ Model file not found: `{MODEL_PATH}`\n\n"
            "Please ensure `models/asd_ucla_best_model.joblib` is present."
        )
        st.stop()
    try:
        model = joblib.load(MODEL_PATH)
        _patch_sklearn_objects(model)  # fix cross-version pickle issues
        return model
    except Exception as e:
        st.error(f"⚠️ Failed to load model: {e}")
        st.stop()


@st.cache_resource(show_spinner=False)
def load_feature_columns():
    """Load the exact ordered list of feature column names used during training."""
    if not os.path.exists(FEATURES_PATH):
        st.error(
            f"⚠️ Feature columns file not found: `{FEATURES_PATH}`\n\n"
            "Please ensure `models/asd_ucla_feature_columns.joblib` is present."
        )
        st.stop()
    try:
        return joblib.load(FEATURES_PATH)
    except Exception as e:
        st.error(f"⚠️ Failed to load feature columns: {e}")
        st.stop()


@st.cache_data(show_spinner=False, ttl=3600)
def load_reference_data() -> dict:
    """
    Load the reference CSV and compute medians for every numeric column.
    Returns a dict {column_name: median_value}.
    -9999 values are treated as NaN (consistent with notebook preprocessing).
    """
    if not os.path.exists(DATA_PATH):
        return {}
    try:
        df = pd.read_csv(DATA_PATH)
        df = df.replace(-9999, np.nan)
        medians: dict = {}
        for col in df.select_dtypes(include=[np.number]).columns:
            med = df[col].median()
            if pd.notna(med):
                medians[col] = float(med)
        return medians
    except Exception:
        return {}
