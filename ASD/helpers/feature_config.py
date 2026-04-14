"""
Feature configuration — defines which features are exposed in the UI,
their display labels, helper text, data types, valid ranges, and defaults.

Features not listed here but required by the model are filled with dataset
medians internally (transparent to the user).
"""

from collections import OrderedDict

# ── Group definitions ────────────────────────────────────────────────────────
# Each entry: column_name -> {label, help, type, min, max, default, step}
# type: "float", "int", "select"

FEATURE_GROUPS: OrderedDict = OrderedDict()

# ─── 1. Basic Information ────────────────────────────────────────────────────
FEATURE_GROUPS["👤 Basic Information"] = OrderedDict({
    "AGE_AT_SCAN": {
        "label": "Age at Assessment (years)",
        "help": "Age of the individual at the time of clinical assessment / scan.",
        "type": "float",
        "min": 1.0,
        "max": 64.0,
        "default": 13.0,
        "step": 0.1,
    },
    "SEX": {
        "label": "Sex",
        "help": "Biological sex — 1 = Male, 2 = Female.",
        "type": "select",
        "options": {"Male": 1, "Female": 2},
        "default": "Male",
    },
    "DSM_IV_TR": {
        "label": "DSM-IV-TR Diagnosis Code",
        "help": "DSM-IV-TR diagnostic classification (0 = None / Control, 1 = Autism, 2 = Asperger's, 3 = PDD-NOS, 4 = Asperger's / PDD-NOS).",
        "type": "select",
        "options": {"None / Control": 0, "Autism": 1, "Asperger's": 2, "PDD-NOS": 3, "Asperger's / PDD-NOS": 4},
        "default": "Autism",
    },
})

# ─── 2. Cognitive / IQ Scores ────────────────────────────────────────────────
FEATURE_GROUPS["🧠 Cognitive / IQ Scores"] = OrderedDict({
    "FIQ": {
        "label": "Full-Scale IQ (FIQ)",
        "help": "Composite IQ score combining verbal and performance abilities. Average is ~100.",
        "type": "float",
        "min": 40.0,
        "max": 160.0,
        "default": 103.0,
        "step": 1.0,
    },
    "VIQ": {
        "label": "Verbal IQ (VIQ)",
        "help": "Verbal comprehension and reasoning score. Average is ~100.",
        "type": "float",
        "min": 40.0,
        "max": 160.0,
        "default": 104.0,
        "step": 1.0,
    },
    "PIQ": {
        "label": "Performance IQ (PIQ)",
        "help": "Non-verbal / visual-spatial reasoning score. Average is ~100.",
        "type": "float",
        "min": 40.0,
        "max": 160.0,
        "default": 101.0,
        "step": 1.0,
    },
})

# ─── 3. ADOS Assessment Scores ───────────────────────────────────────────────
FEATURE_GROUPS["📋 ADOS Assessment Scores"] = OrderedDict({
    "ADOS_TOTAL": {
        "label": "ADOS Total Score",
        "help": "Autism Diagnostic Observation Schedule — total composite score. Higher values indicate more ASD-related behaviors.",
        "type": "int",
        "min": 0,
        "max": 30,
        "default": 11,
        "step": 1,
    },
    "ADOS_COMM": {
        "label": "ADOS Communication",
        "help": "Communication subscale of ADOS. Measures language and communication deficits.",
        "type": "int",
        "min": 0,
        "max": 10,
        "default": 3,
        "step": 1,
    },
    "ADOS_SOCIAL": {
        "label": "ADOS Social Interaction",
        "help": "Social interaction subscale of ADOS. Measures reciprocal social behavior deficits.",
        "type": "int",
        "min": 0,
        "max": 16,
        "default": 8,
        "step": 1,
    },
    "ADOS_STEREO_BEHAV": {
        "label": "ADOS Stereotyped Behavior",
        "help": "Restricted and repetitive behaviors subscale of ADOS.",
        "type": "int",
        "min": 0,
        "max": 10,
        "default": 2,
        "step": 1,
    },
    "ADOS_MODULE": {
        "label": "ADOS Module Used",
        "help": "ADOS module administered (1-4). Module depends on the subject's language level.",
        "type": "select",
        "options": {"Module 1 (Pre-verbal / Single words)": 1, "Module 2 (Phrase speech)": 2, "Module 3 (Fluent child)": 3, "Module 4 (Fluent adolescent/adult)": 4},
        "default": "Module 3 (Fluent child)",
    },
})

# ─── 4. ADOS Gotham Algorithm Scores ─────────────────────────────────────────
FEATURE_GROUPS["📊 ADOS Gotham Revised Scores"] = OrderedDict({
    "ADOS_GOTHAM_SOCAFFECT": {
        "label": "Gotham Social Affect",
        "help": "ADOS-2 Gotham revised social-affect algorithm score (0–20).",
        "type": "int",
        "min": 0,
        "max": 20,
        "default": 9,
        "step": 1,
    },
    "ADOS_GOTHAM_RRB": {
        "label": "Gotham Restricted/Repetitive Behavior",
        "help": "ADOS-2 Gotham RRB algorithm score (0–8).",
        "type": "int",
        "min": 0,
        "max": 8,
        "default": 2,
        "step": 1,
    },
    "ADOS_GOTHAM_TOTAL": {
        "label": "Gotham Total Score",
        "help": "Sum of Gotham Social Affect + RRB.",
        "type": "int",
        "min": 0,
        "max": 28,
        "default": 12,
        "step": 1,
    },
    "ADOS_GOTHAM_SEVERITY": {
        "label": "Gotham Calibrated Severity Score",
        "help": "Calibrated severity (1–10). Higher = more severe ASD presentation.",
        "type": "int",
        "min": 1,
        "max": 10,
        "default": 7,
        "step": 1,
    },
})

# ─── 5. ADI-R Assessment Scores ──────────────────────────────────────────────
FEATURE_GROUPS["📝 ADI-R Interview Scores"] = OrderedDict({
    "ADI_R_SOCIAL_TOTAL_A": {
        "label": "ADI-R Social Total (A)",
        "help": "Autism Diagnostic Interview — social interaction abnormalities. Cut-off for autism: ≥10.",
        "type": "int",
        "min": 0,
        "max": 30,
        "default": 22,
        "step": 1,
    },
    "ADI_R_VERBAL_TOTAL_BV": {
        "label": "ADI-R Verbal Total (BV)",
        "help": "ADI-R communication / verbal domain score. Cut-off for autism: ≥8 (verbal), ≥7 (non-verbal).",
        "type": "int",
        "min": 0,
        "max": 26,
        "default": 17,
        "step": 1,
    },
    "ADI_RRB_TOTAL_C": {
        "label": "ADI-R RRB Total (C)",
        "help": "Restricted, repetitive behaviors domain. Cut-off for autism: ≥3.",
        "type": "int",
        "min": 0,
        "max": 15,
        "default": 8,
        "step": 1,
    },
    "ADI_R_ONSET_TOTAL_D": {
        "label": "ADI-R Onset Total (D)",
        "help": "Age of onset / early development abnormality score. Cut-off for autism: ≥1.",
        "type": "int",
        "min": 0,
        "max": 5,
        "default": 3,
        "step": 1,
    },
})

# ─── 6. Additional Clinical Inputs ───────────────────────────────────────────
FEATURE_GROUPS["🏥 Additional Clinical Inputs"] = OrderedDict({
    "CURRENT_MED_STATUS": {
        "label": "Currently on Medication?",
        "help": "Whether the individual is currently on psychotropic medication. 0 = No, 1 = Yes.",
        "type": "select",
        "options": {"No": 0, "Yes": 1},
        "default": "No",
    },
    "EYE_STATUS_AT_SCAN": {
        "label": "Eye Status at Scan",
        "help": "Eye status during MRI scan. 1 = Open, 2 = Closed.",
        "type": "select",
        "options": {"Open": 1, "Closed": 2},
        "default": "Open",
    },
})


# ─── Collect all UI feature names ─────────────────────────────────────────────
def get_all_ui_features():
    """Return a flat set of all feature column names exposed in the UI."""
    features = set()
    for group_features in FEATURE_GROUPS.values():
        features.update(group_features.keys())
    return features


# ─── Feature descriptions for explanation ─────────────────────────────────────
FEATURE_DESCRIPTIONS = {
    "AGE_AT_SCAN": "Age at assessment",
    "SEX": "Biological sex",
    "DSM_IV_TR": "DSM-IV-TR classification",
    "FIQ": "Full-Scale IQ",
    "VIQ": "Verbal IQ",
    "PIQ": "Performance IQ",
    "ADOS_TOTAL": "ADOS total score",
    "ADOS_COMM": "ADOS communication",
    "ADOS_SOCIAL": "ADOS social interaction",
    "ADOS_STEREO_BEHAV": "ADOS stereotyped behavior",
    "ADOS_MODULE": "ADOS module",
    "ADOS_GOTHAM_SOCAFFECT": "Gotham social affect",
    "ADOS_GOTHAM_RRB": "Gotham RRB",
    "ADOS_GOTHAM_TOTAL": "Gotham total",
    "ADOS_GOTHAM_SEVERITY": "Gotham severity",
    "ADI_R_SOCIAL_TOTAL_A": "ADI-R social total",
    "ADI_R_VERBAL_TOTAL_BV": "ADI-R verbal total",
    "ADI_RRB_TOTAL_C": "ADI-R RRB total",
    "ADI_R_ONSET_TOTAL_D": "ADI-R onset",
    "CURRENT_MED_STATUS": "Medication status",
    "EYE_STATUS_AT_SCAN": "Eye status at scan",
    # Hidden / technical features
    "Unnamed: 0.1": "Index column (auto-filled)",
    "sr": "Serial number (auto-filled)",
    "Unnamed: 0": "Index column (auto-filled)",
    "SUB_ID": "Subject ID (auto-filled)",
    "X": "Row index (auto-filled)",
    "ADI_R_RSRCH_RELIABLE": "ADI-R research reliability flag",
    "ADOS_RSRCH_RELIABLE": "ADOS research reliability flag",
    "AGE_AT_MPRAGE": "Age at MRI scan",
    "SUB_IN_SMP": "Subject in sample flag",
    "anat_cnr": "Anatomical contrast-to-noise ratio",
    "anat_efc": "Anatomical entropy focus criterion",
    "anat_fber": "Anatomical foreground-background energy ratio",
    "anat_fwhm": "Anatomical full width at half maximum",
    "anat_qi1": "Anatomical quality index 1",
    "anat_snr": "Anatomical signal-to-noise ratio",
    "func_efc": "Functional entropy focus criterion",
    "func_fber": "Functional foreground-background energy ratio",
    "func_fwhm": "Functional full width at half maximum",
    "func_dvars": "Functional DVARS (temporal derivative variance)",
    "func_outlier": "Functional outlier fraction",
    "func_quality": "Functional quality index",
    "func_mean_fd": "Functional mean framewise displacement",
    "func_num_fd": "Functional number of FD outliers",
    "func_perc_fd": "Functional percent FD outliers",
    "func_gsr": "Functional global signal regression",
}
