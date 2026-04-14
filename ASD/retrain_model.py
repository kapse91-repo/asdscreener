"""
Retrain ASD model locally — fixes the SimpleImputer pickle incompatibility.

Run:  .venv\Scripts\python.exe retrain_model.py
"""

import os
import sys
import numpy as np
import pandas as pd
import joblib
import sklearn

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, roc_auc_score, confusion_matrix

print(f"Python   : {sys.version}")
print(f"sklearn  : {sklearn.__version__}")
print(f"numpy    : {np.__version__}")
print(f"pandas   : {pd.__version__}")
print()

# ── Paths ──────────────────────────────────────────────────────────────────────
BASE_DIR    = os.path.dirname(os.path.abspath(__file__))
DATA_PATH   = os.path.join(BASE_DIR, "data", "UCLA_Master_Features-1-1-5.csv")
MODEL_OUT   = os.path.join(BASE_DIR, "models", "asd_ucla_best_model.joblib")
FEAT_OUT    = os.path.join(BASE_DIR, "models", "asd_ucla_feature_columns.joblib")

# ── 1. Load data ───────────────────────────────────────────────────────────────
print(f"Loading data from: {DATA_PATH}")
if not os.path.exists(DATA_PATH):
    print(f"ERROR: Data file not found at {DATA_PATH}")
    sys.exit(1)

df = pd.read_csv(DATA_PATH)
print(f"Raw shape: {df.shape}")

# ── 2. Clean ───────────────────────────────────────────────────────────────────
df = df.replace(-9999, np.nan)

# Drop ID / index-like columns
id_cols = ["subject", "SITE_ID", "FILE_ID"]
id_cols = [c for c in id_cols if c in df.columns]
df = df.drop(columns=id_cols, errors="ignore")

# Drop high-missing columns (>50%)
high_missing = df.columns[df.isna().mean() > 0.5].tolist()
df = df.drop(columns=high_missing)
print(f"Dropped {len(high_missing)} high-missing columns")

# Drop text columns (except target)
text_cols = [c for c in df.columns if df[c].dtype == "object" and c != "DX_GROUP"]
df = df.drop(columns=text_cols)
print(f"Dropped text columns: {text_cols}")

# ── 3. Target ──────────────────────────────────────────────────────────────────
assert "DX_GROUP" in df.columns, "DX_GROUP column missing!"
df = df.dropna(subset=["DX_GROUP"])
df["label"] = df["DX_GROUP"].map({1: 1, 2: 0})
df = df.drop(columns=["DX_GROUP"])
df = df.dropna(subset=["label"])
df["label"] = df["label"].astype(int)

X = df.drop(columns=["label"])
y = df["label"]
num_cols = X.columns.tolist()
print(f"\nFeatures: {len(num_cols)}")
print(f"Samples : {len(y)}  (ASD={y.sum()}, Non-ASD={(y==0).sum()})")

# ── 4. Train / Test split ──────────────────────────────────────────────────────
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)
print(f"\nTrain: {X_train.shape}  |  Test: {X_test.shape}")

# ── 5. Pipeline ────────────────────────────────────────────────────────────────
numeric_transformer = Pipeline([
    ("imputer", SimpleImputer(strategy="mean")),
    ("scaler",  StandardScaler()),
])

preprocessor = ColumnTransformer([
    ("num", numeric_transformer, num_cols)
])

pipeline = Pipeline([
    ("preprocess", preprocessor),
    ("model",     LogisticRegression(max_iter=1000, class_weight="balanced", random_state=42)),
])

# ── 6. Train ───────────────────────────────────────────────────────────────────
print("\nTraining Logistic Regression pipeline...")
pipeline.fit(X_train, y_train)

# ── 7. Evaluate ────────────────────────────────────────────────────────────────
y_pred  = pipeline.predict(X_test)
y_proba = pipeline.predict_proba(X_test)[:, 1]

print(f"\nROC-AUC  : {roc_auc_score(y_test, y_proba):.4f}")
print(classification_report(y_test, y_pred))
print("Confusion matrix:\n", confusion_matrix(y_test, y_pred))

# ── 8. Save ────────────────────────────────────────────────────────────────────
joblib.dump(pipeline, MODEL_OUT)
joblib.dump(num_cols, FEAT_OUT)
print(f"\n✅ Model saved  : {MODEL_OUT}")
print(f"✅ Features saved: {FEAT_OUT}")
print(f"\nDone! Now restart the Streamlit app.")
