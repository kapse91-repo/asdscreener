"""
PDF & Text report generation using fpdf2.
"""
from __future__ import annotations
from datetime import datetime
from fpdf import FPDF


def _s(text) -> str:
    """Sanitize text for Helvetica PDF output — replace non-latin-1 chars."""
    if text is None:
        return "-"
    t = str(text)
    replacements = {
        "\u2014": "-",   # em dash
        "\u2013": "-",   # en dash
        "\u2012": "-",   # figure dash
        "\u2011": "-",   # non-breaking hyphen
        "\u2018": "'",   # left single quote
        "\u2019": "'",   # right single quote
        "\u201c": '"',   # left double quote
        "\u201d": '"',   # right double quote
        "\u2022": "*",   # bullet
        "\u00b7": ".",   # middle dot
        "\u2026": "...", # ellipsis
    }
    for k, v in replacements.items():
        t = t.replace(k, v)
    # Final fallback: encode to latin-1, ignore unmappable
    return t.encode("latin-1", errors="replace").decode("latin-1")


# ── Colour palette ────────────────────────────────────────────────────
ASD_COLOR    = (220, 38, 38)       # red
NONASD_COLOR = (22, 163, 74)       # green
BRAND_COLOR  = (10, 61, 98)        # dark navy
ACCENT_COLOR = (21, 101, 160)      # medium blue
LIGHT_GRAY   = (245, 247, 250)
MID_GRAY     = (100, 116, 139)
DARK_TEXT    = (15, 23, 42)


class ASDReport(FPDF):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_auto_page_break(auto=True, margin=18)

    def header(self):
        # Navy top bar
        self.set_fill_color(*BRAND_COLOR)
        self.rect(0, 0, 210, 14, "F")
        self.set_font("Helvetica", "B", 9)
        self.set_text_color(255, 255, 255)
        self.set_xy(10, 3)
        self.cell(0, 8, _s("ASD PREDICTION SYSTEM - AI-Assisted Autism Screening Research Tool"), ln=True)
        self.set_text_color(*DARK_TEXT)
        self.ln(6)

    def footer(self):
        self.set_y(-14)
        self.set_fill_color(245, 247, 250)
        self.rect(0, self.get_y(), 210, 20, "F")
        self.set_font("Helvetica", "", 7)
        self.set_text_color(*MID_GRAY)
        self.cell(0, 6, _s(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}   |   For research & educational purposes ONLY   |   Page {self.page_no()}"), align="C")

    def section_title(self, title: str):
        self.set_font("Helvetica", "B", 11)
        self.set_text_color(*ACCENT_COLOR)
        self.set_fill_color(*LIGHT_GRAY)
        self.set_draw_color(*ACCENT_COLOR)
        self.rect(10, self.get_y(), 190, 8, "F")
        self.set_x(13)
        self.cell(0, 8, _s(title), ln=True)
        self.ln(2)

    def two_col_row(self, label: str, value: str, alt: bool = False):
        if alt:
            self.set_fill_color(248, 250, 252)
        else:
            self.set_fill_color(255, 255, 255)
        self.rect(10, self.get_y(), 190, 7, "F")
        self.set_font("Helvetica", "", 9)
        self.set_text_color(*MID_GRAY)
        self.set_x(13)
        self.cell(85, 7, _s(label))
        self.set_font("Helvetica", "B", 9)
        self.set_text_color(*DARK_TEXT)
        self.cell(100, 7, _s(value), ln=True)


def generate_pdf_report(
    result: dict,
    user_inputs: dict,
    interpretation: str,
    recommendation: str,
    user: dict | None = None,
) -> bytes:
    """Generate a polished PDF report. Returns PDF bytes."""
    from helpers.feature_config import FEATURE_GROUPS, FEATURE_DESCRIPTIONS

    label   = result["label_text"]
    conf    = result["confidence"] * 100
    asd_p   = result["probability"] * 100
    nonasd  = 100 - asd_p
    is_asd  = result["label"] == 1
    res_col = ASD_COLOR if is_asd else NONASD_COLOR

    # Build label maps
    label_map, sel_rev = {}, {}
    for gf in FEATURE_GROUPS.values():
        for fn, fc in gf.items():
            label_map[fn] = fc["label"]
            if fc["type"] == "select":
                sel_rev[fn] = {v: k for k, v in fc["options"].items()}

    pdf = ASDReport(orientation="P", unit="mm", format="A4")
    pdf.add_page()

    # ── Hero result banner ────────────────────────────────────────────
    pdf.set_fill_color(*res_col)
    pdf.rect(10, pdf.get_y(), 190, 30, "F")
    result_icon = "! ASD DETECTED" if is_asd else "* NON-ASD"
    pdf.set_font("Helvetica", "B", 18)
    pdf.set_text_color(255, 255, 255)
    pdf.set_xy(20, pdf.get_y() + 5)
    pdf.cell(0, 10, _s(result_icon), ln=True)
    pdf.set_font("Helvetica", "", 9)
    sub = "Autism Spectrum Disorder indicators identified" if is_asd else "No significant ASD indicators detected"
    pdf.set_x(20)
    pdf.cell(0, 7, _s(sub), ln=True)
    pdf.ln(6)

    # ── Confidence strip ──────────────────────────────────────────────
    pdf.set_text_color(*DARK_TEXT)
    pdf.section_title("PREDICTION CONFIDENCE")
    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(*MID_GRAY)
    pdf.set_x(13)
    pdf.cell(0, 6, _s(f"Model Confidence: {conf:.1f}%   |   ASD Probability: {asd_p:.1f}%   |   Non-ASD Probability: {nonasd:.1f}%"), ln=True)

    # Visual confidence bar
    bar_x, bar_y, bar_w = 13, pdf.get_y() + 2, 184
    pdf.set_fill_color(235, 238, 242)
    pdf.rect(bar_x, bar_y, bar_w, 5, "F")
    fill_w = bar_w * conf / 100
    pdf.set_fill_color(*res_col)
    pdf.rect(bar_x, bar_y, fill_w, 5, "F")
    pdf.ln(10)

    # ── User info ─────────────────────────────────────────────────────
    if user:
        pdf.section_title("CLINICIAN INFORMATION")
        rows = [
            ("Name",        user.get("full_name") or user.get("username", "—")),
            ("Role",        user.get("role", "—").capitalize()),
            ("Institution", user.get("institution", "—") or "—"),
            ("Email",       user.get("email", "—")),
            ("Report Date", datetime.now().strftime("%Y-%m-%d %H:%M")),
        ]
        for i, (k, v) in enumerate(rows):
            pdf.two_col_row(k, v, alt=(i % 2 == 0))
        pdf.ln(5)

    # ── Interpretation ────────────────────────────────────────────────
    pdf.section_title("CLINICAL INTERPRETATION")
    plain = interpretation.replace("**", "")
    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(*DARK_TEXT)
    pdf.set_x(13)
    pdf.multi_cell(184, 5.5, _s(plain))
    pdf.ln(3)

    # ── Patient inputs ────────────────────────────────────────────────
    pdf.section_title("PATIENT ASSESSMENT INPUTS")
    for i, (fn, val) in enumerate(user_inputs.items()):
        disp_val = sel_rev.get(fn, {}).get(val, val)
        pdf.two_col_row(_s(label_map.get(fn, fn)), _s(disp_val), alt=(i % 2 == 0))
    pdf.ln(5)

    # ── Hidden/auto-filled features ───────────────────────────────────
    pdf.section_title("AUTO-FILLED FEATURES (MODEL DEFAULTS)")
    hidden = result.get("hidden_info", {})
    for i, (col, info) in enumerate(hidden.items()):
        val = info["value"]
        val_str = f"{val:.4f}" if isinstance(val, float) and val == val else str(val)
        desc = info.get("description", col)
        pdf.two_col_row(_s(desc[:50]), _s(f"{val_str}  (Median)"), alt=(i % 2 == 0))
    pdf.ln(5)

    # ── Disclaimer ────────────────────────────────────────────────────
    pdf.section_title("MEDICAL DISCLAIMER")
    disclaimer = (
        "This prediction report is generated by a machine learning model trained on a limited "
        "research dataset (UCLA ABIDE, n=109). It is intended for RESEARCH AND EDUCATIONAL "
        "PURPOSES ONLY. This is NOT a clinical diagnosis. Autism Spectrum Disorder can only be "
        "definitively diagnosed by qualified healthcare professionals through comprehensive "
        "clinical assessment. Always consult a licensed clinician for diagnostic concerns."
    )
    pdf.set_fill_color(255, 251, 235)
    pdf.set_draw_color(251, 191, 36)
    pdf.set_x(10)
    pdf.set_font("Helvetica", "", 8.5)
    pdf.set_text_color(92, 64, 14)
    pdf.multi_cell(190, 5.5, _s(disclaimer), border=1, fill=True)
    pdf.ln(4)

    # ── Model info ────────────────────────────────────────────────────
    pdf.section_title("MODEL INFORMATION")
    model_rows = [
        ("Algorithm",    "Logistic Regression (class_weight=balanced)"),
        ("Pipeline",     "SimpleImputer -> StandardScaler -> LogisticRegression"),
        ("Total Features", "46 clinical, behavioral & phenotypic features"),
        ("Dataset",      "UCLA ABIDE - 109 subjects (62 ASD + 47 Control)"),
        ("Test ROC-AUC", "1.00"),
        ("Test Accuracy","100% (held-out 20% test set, n=22)"),
    ]
    for i, (k, v) in enumerate(model_rows):
        pdf.two_col_row(k, v, alt=(i % 2 == 0))

    return bytes(pdf.output())


# ── Plain text fallback ───────────────────────────────────────────────
def generate_text_report(result, user_inputs, interpretation, recommendation):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    lines = [
        "=" * 68,
        "  ASD PREDICTION REPORT",
        f"  Generated: {now}",
        "=" * 68,
        f"  Prediction  : {result['label_text']}",
        f"  ASD Prob    : {result['probability']*100:.1f}%",
        f"  Confidence  : {result['confidence']*100:.1f}%",
        "",
        "  INTERPRETATION",
        f"  {interpretation.replace('**','')}",
        "",
        "  DISCLAIMER:",
        "  For research/educational use only. NOT a clinical diagnosis.",
        "=" * 68,
    ]
    return "\n".join(lines)
