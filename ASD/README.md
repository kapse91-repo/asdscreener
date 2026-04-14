# 🧬 ASD Prediction System — AI-Assisted Autism Screening

A professional, production-quality Streamlit web application for **Autism Spectrum Disorder (ASD) prediction** using a pretrained machine learning model. Built on the UCLA ABIDE phenotypic dataset with clinical, behavioral, and imaging quality control features.

> ⚠️ **Disclaimer:** This tool is for **research and educational purposes only**. It is NOT a clinical diagnostic tool and should never replace professional medical evaluation.

---

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the Application

```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`.

---

## 📁 Project Structure

```
ASD/
├── app.py                          # Main Streamlit application
├── requirements.txt                # Python dependencies
├── README.md                       # This file
├── helpers/
│   ├── __init__.py
│   ├── model_loader.py             # Model & data loading with caching
│   ├── feature_config.py           # Feature definitions, groups, UI config
│   ├── predictor.py                # Prediction engine & interpretation
│   └── report_generator.py         # Downloadable report generator
├── models/
│   ├── asd_ucla_best_model.joblib  # Pretrained LogisticRegression pipeline
│   └── asd_ucla_feature_columns.joblib  # Ordered feature column list (46)
├── data/
│   ├── UCLA_Master_Features-1-1-5.csv              # Primary reference dataset
│   └── UCLAPhenotypic_V1_0b_preprocessed1 (1) (2) (1).csv  # Supplementary data
└── notebooks/
    └── asd_ucla_training.ipynb     # Training notebook (reference)
```

---

## 🏗️ How It Works

### Model Loading
- The **pretrained model** is loaded from `models/asd_ucla_best_model.joblib`
- The **exact feature column order** is loaded from `models/asd_ucla_feature_columns.joblib`
- Both are cached using Streamlit's `@st.cache_resource` for fast reloads

### Feature Handling
| Category | Count | Details |
|----------|-------|---------|
| **User-exposed features** | 22 | Shown in the UI with labels, help text, and valid ranges |
| **Auto-filled features** | 24 | Filled with dataset medians from `UCLA_Master_Features-1-1-5.csv` |
| **Total model features** | 46 | Exact training feature set |

### User-Exposed Features
- **Basic Info:** Age, Sex, DSM-IV-TR code
- **Cognitive / IQ:** FIQ, VIQ, PIQ
- **ADOS Scores:** Total, Communication, Social, Stereotyped Behavior, Module
- **ADOS Gotham:** Social Affect, RRB, Total, Severity
- **ADI-R Scores:** Social Total, Verbal Total, RRB Total, Onset
- **Clinical:** Medication Status, Eye Status

### Hidden Features (Auto-Filled)
Features like imaging QC metrics (`anat_cnr`, `func_efc`, etc.), subject IDs, and index columns are automatically filled with **dataset median values**. These are fully transparent — visible in the Technical Details tab and downloadable reports.

### Prediction Flow
1. User fills the grouped form (22 clinical features)
2. Remaining 24 features are auto-filled with medians
3. A single-row DataFrame is built in exact training column order
4. The sklearn Pipeline processes: **Impute → Scale → Predict**
5. Results include label, probabilities, interpretation, and recommendations

---

## 📈 Model Performance

| Metric | Value |
|--------|-------|
| **Model Type** | Logistic Regression (balanced class weights) |
| **Pipeline** | SimpleImputer → StandardScaler → LogisticRegression |
| **Test ROC-AUC** | 1.00 |
| **Test Accuracy** | 100% (22 subjects held out) |
| **Training Data** | 87 subjects (80% stratified split) |
| **Dataset** | UCLA site, ABIDE consortium (109 subjects) |

> **Note:** Perfect test metrics on a small dataset (n=22) should be interpreted cautiously. This does not guarantee generalization to broader populations.

---

## 🔬 Features

- ✅ **Real ML inference** — uses the actual pretrained model, no dummy classifiers
- ✅ **Professional health-tech UI** — clean, modern, medical-grade design
- ✅ **Grouped form inputs** — organized by assessment tool (ADOS, ADI-R, IQ, etc.)
- ✅ **Transparent defaults** — all auto-filled values visible in Technical Details
- ✅ **Downloadable reports** — formatted prediction reports with full details
- ✅ **Model documentation** — architecture, pipeline, and performance sections
- ✅ **Dataset documentation** — source, preprocessing, and feature explanations
- ✅ **Evaluator-friendly** — technical tab shows exact feature vectors and defaults
- ✅ **Disclaimers** — clear research-only positioning throughout the app

---

## ⚠️ Limitations

- **Small dataset** — 109 subjects from a single UCLA ABIDE site
- **Single site** — may not generalize to other populations or acquisition protocols
- **Research-grade** — designed for screening support, not clinical diagnosis
- **Auto-filled features** — imaging QC features use median defaults, which may affect accuracy
- **No SRS features in model** — SRS scores were dropped during training due to high missingness (>50%)

---

## 🛠️ Technology Stack

- **Python 3.8+**
- **Streamlit** — Web interface
- **scikit-learn** — Machine learning pipeline
- **pandas / numpy** — Data manipulation
- **joblib** — Model serialization

---

## 📖 How to Use

1. **Open the app** — navigate to `http://localhost:8501`
2. **Go to "Prediction Workspace"** — the first tab
3. **Fill in assessment scores** — use the grouped form sections
4. **Review inputs** — expand the input summary panel
5. **Click "Run Prediction"** — get your result
6. **Read the interpretation** — understand what the model says
7. **Download the report** — save a formatted prediction report
8. **Explore other tabs** — learn about the model, dataset, and performance

---

*Built for academic demonstration and portfolio presentation.*
