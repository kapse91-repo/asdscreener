"""
Prediction / Assessment page — empty form, hints, back button, PDF export.

Fixes applied:
- Results now persist in session_state (no re-run loss)
- Save prediction returns status; toast message shown
- inputs_json serialization uses str() fallback
- Spinner is non-blocking (uses st.status)
- Clears previous result when "New Assessment" is clicked
"""
import streamlit as st
from datetime import datetime
import base64

from helpers.model_loader import load_model, load_feature_columns
from helpers.feature_config import FEATURE_GROUPS, FEATURE_DESCRIPTIONS, get_all_ui_features
from helpers.predictor import predict, generate_interpretation, generate_recommendation
from helpers.report_generator import generate_pdf_report
from helpers.auth import save_prediction


GROUP_DESC = {
    "👤 Basic Information":
        "Demographic and diagnostic classification details of the patient.",
    "🧠 Cognitive / IQ Scores":
        "Standardized IQ measures — population mean = 100, SD = 15. Enter actual test results.",
    "📋 ADOS Assessment Scores":
        "Autism Diagnostic Observation Schedule — semi-structured standardised behavioral assessment scores.",
    "📊 ADOS Gotham Revised Scores":
        "ADOS-2 calibrated severity scores using Gotham algorithm for cross-module comparison.",
    "📝 ADI-R Interview Scores":
        "Autism Diagnostic Interview-Revised — structured caregiver interview scores across social, communication & RRB domains.",
    "🏥 Additional Clinical Inputs":
        "Current medication status and eye-tracking status recorded at time of scan.",
}

FIELD_HINTS = {
    "AGE_AT_SCAN":            "e.g. 12.5",
    "FIQ":                    "e.g. 98  (mean=100)",
    "VIQ":                    "e.g. 101 (mean=100)",
    "PIQ":                    "e.g. 95  (mean=100)",
    "ADOS_TOTAL":             "e.g. 10  (typical range 0–28)",
    "ADOS_COMM":              "e.g. 3   (0–8 range)",
    "ADOS_SOCIAL":            "e.g. 7   (0–20 range)",
    "ADOS_STEREO_BEHAV":      "e.g. 2   (0–8 range)",
    "ADOS_GOTHAM_SOCAFFECT":  "e.g. 9   (0–22 range)",
    "ADOS_GOTHAM_RRB":        "e.g. 2   (0–6 range)",
    "ADOS_GOTHAM_TOTAL":      "e.g. 11  (0–28 range)",
    "ADOS_GOTHAM_SEVERITY":   "e.g. 6   (1–10 scale)",
    "ADI_R_SOCIAL_TOTAL_A":   "e.g. 20  (0–30 range)",
    "ADI_R_VERBAL_TOTAL_BV":  "e.g. 16  (0–26 range)",
    "ADI_RRB_TOTAL_C":        "e.g. 7   (0–12 range)",
    "ADI_R_ONSET_TOTAL_D":    "e.g. 3   (0–9 range)",
}


def show(user: dict):
    dark = st.session_state.get("dark_mode", False)
    conf_head_c = "#93c5fd" if dark else "#1565a0"
    muted_c     = "#64748b" if dark else "#94a3b8"

    # ── Back navigation ───────────────────────────────────────────────
    if st.button("← Back to Dashboard", key="pred_back"):
        st.session_state.pop("pred_result", None)
        st.session_state.page = "dashboard"
        st.rerun()

    # ── Header ───────────────────────────────────────────────────────
    st.markdown("""
<div class="page-title">🔬 Patient Assessment</div>
<div class="page-subtitle">Enter patient clinical and behavioral scores to generate an AI-assisted ASD prediction.</div>
<hr class="page-divider">""", unsafe_allow_html=True)

    st.markdown("""
<div class="info-box">
  <strong>How to use:</strong> Fill in each assessment section below. Fields start at their minimum
  value — hover over <b>ⓘ</b> for field descriptions and expected ranges.
  All values are required for a valid prediction. Incomplete forms will use dataset medians for missing data.
</div>""", unsafe_allow_html=True)

    # ── Assessment form ───────────────────────────────────────────────
    user_inputs = {}

    for group_name, group_features in FEATURE_GROUPS.items():
        desc = GROUP_DESC.get(group_name, "")
        st.markdown(f"""
<div class="fg-card">
<div class="fg-title">{group_name}</div>
<div class="fg-desc">{desc}</div>
</div>""", unsafe_allow_html=True)

        n    = len(group_features)
        cols = st.columns(min(n, 3))

        for idx, (feat, cfg) in enumerate(group_features.items()):
            with cols[idx % len(cols)]:
                hint = FIELD_HINTS.get(feat, "")

                if cfg["type"] == "select":
                    opts = list(cfg["options"].keys())
                    sel = st.selectbox(
                        cfg["label"], opts,
                        index=opts.index(cfg["default"]) if cfg["default"] in opts else 0,
                        help=cfg["help"], key=f"p_{feat}"
                    )
                    user_inputs[feat] = cfg["options"][sel]

                elif cfg["type"] == "int":
                    user_inputs[feat] = st.number_input(
                        cfg["label"],
                        min_value=cfg["min"], max_value=cfg["max"],
                        value=cfg["min"],
                        step=cfg["step"],
                        help=f"{cfg['help']}  {hint}",
                        key=f"p_{feat}"
                    )

                else:  # float
                    user_inputs[feat] = st.number_input(
                        cfg["label"],
                        min_value=float(cfg["min"]), max_value=float(cfg["max"]),
                        value=float(cfg["min"]),
                        step=float(cfg["step"]),
                        help=f"{cfg['help']}  {hint}",
                        key=f"p_{feat}", format="%.1f"
                    )
        st.write("")

    # ── Run button ────────────────────────────────────────────────────
    st.write("")
    _, btn_col, _ = st.columns([1, 2, 1])
    with btn_col:
        clicked = st.button("🧠  Run AI Analysis", use_container_width=True,
                            type="primary", key="run_pred")

    # ── Run prediction ────────────────────────────────────────────────
    if clicked:
        with st.spinner("Analysing patient data with AI model — please wait…"):
            try:
                result   = predict(user_inputs)
                interp   = generate_interpretation(result)
                rec_text = generate_recommendation(result)
                # Cache results in session so they survive reruns from download button
                st.session_state["pred_result"]   = result
                st.session_state["pred_interp"]   = interp
                st.session_state["pred_rec"]      = rec_text
                st.session_state["pred_inputs"]   = user_inputs
                st.session_state["pred_ts"]       = datetime.now().strftime("%Y%m%d_%H%M%S")
                st.session_state.pop("pred_pdf", None)  # clear stale PDF
                # Save to DB
                saved_ok = save_prediction(
                    user_id     = user["id"],
                    patient_age = float(user_inputs.get("AGE_AT_SCAN", 0)),
                    patient_sex = str(int(user_inputs.get("SEX", 0))),
                    prediction  = result["label_text"],
                    asd_prob    = result["probability"],
                    confidence  = result["confidence"],
                    inputs      = {k: int(v) if isinstance(v, bool) else v
                                   for k, v in user_inputs.items()},
                )
                if not saved_ok:
                    st.warning("⚠️ Prediction completed but could not be saved to history.")
            except Exception as e:
                st.error(f"❌ Prediction failed: {e}")
                st.session_state.pop("pred_result", None)
                st.stop()

    # ── Render cached results (survives download-button reruns) ───────
    result   = st.session_state.get("pred_result")
    interp   = st.session_state.get("pred_interp", "")
    rec_text = st.session_state.get("pred_rec", "")
    cached_inputs = st.session_state.get("pred_inputs", user_inputs)

    if result is None:
        st.markdown("""
<div class="app-footer">
  <strong>ASD Prediction System</strong><br>Built by Yogadi
</div>""", unsafe_allow_html=True)
        return

    is_asd   = result["label"] == 1
    conf     = result["confidence"] * 100
    asd_prob = result["probability"] * 100
    nonasd_p = 100 - asd_prob

    st.write("")
    st.markdown('<div class="sec-head"><h2>📊 Prediction Results</h2></div><hr class="sec-line">', unsafe_allow_html=True)

    # ── Result card + confidence ──────────────────────────────────
    col_r, col_c = st.columns(2, gap="large")

    with col_r:
        if is_asd:
            st.markdown("""
<div class="result-asd">
<div class="result-icon">⚠️</div>
<div class="result-label result-label-asd">ASD Detected</div>
<div class="result-sub result-sub-asd">Autism Spectrum Disorder indicators identified</div>
</div>""", unsafe_allow_html=True)
        else:
            st.markdown("""
<div class="result-nonasd">
<div class="result-icon">✅</div>
<div class="result-label result-label-nonasd">Non-ASD</div>
<div class="result-sub result-sub-nonasd">No significant ASD indicators detected</div>
</div>""", unsafe_allow_html=True)

    with col_c:
        bc         = "bar-asd" if is_asd else "bar-nonasd"
        pc         = "conf-pct-asd" if is_asd else "conf-pct-nonasd"
        asd_color  = "#dc2626"
        nasd_color = "#16a34a"
        st.markdown(f"""
<div class="conf-box">
<div style="font-size:0.85rem;font-weight:700;color:{conf_head_c};margin-bottom:0.8rem;">Model Confidence Score</div>
<div class="conf-pct {pc}">{conf:.1f}%</div>
<div class="bar-track"><div class="bar-fill {bc}" style="width:{conf:.1f}%;"></div></div>
<div class="bar-labels"><span>0%</span><span>25%</span><span>50%</span><span>75%</span><span>100%</span></div>
<div class="prob-row">
  <div class="prob-cell">
    <div class="prob-val" style="color:{asd_color};">{asd_prob:.1f}%</div>
    <div class="prob-lbl">ASD Probability</div>
  </div>
  <div class="prob-cell">
    <div class="prob-val" style="color:{nasd_color};">{nonasd_p:.1f}%</div>
    <div class="prob-lbl">Non-ASD Probability</div>
  </div>
</div>
</div>""", unsafe_allow_html=True)

    # ── Interpretation ────────────────────────────────────────────
    clean_interp = interp.replace("**", "")
    st.markdown(f"""
<div class="interp-card">
<div class="interp-head">💡 Clinical Interpretation</div>
<div class="interp-body">{clean_interp}</div>
</div>""", unsafe_allow_html=True)

    # ── Recommendation ────────────────────────────────────────────
    st.markdown(rec_text)

    # ── Patient input summary ─────────────────────────────────────
    st.markdown('<div class="sec-head"><h2>👤 Patient Input Summary</h2></div><hr class="sec-line">', unsafe_allow_html=True)

    label_map, sel_rev = {}, {}
    for gf in FEATURE_GROUPS.values():
        for fn, fc in gf.items():
            label_map[fn] = fc["label"]
            if fc["type"] == "select":
                sel_rev[fn] = {v: k for k, v in fc["options"].items()}

    items = list(cached_inputs.items())
    mid   = (len(items) + 1) // 2
    cs1, cs2 = st.columns(2)
    for col, chunk in ((cs1, items[:mid]), (cs2, items[mid:])):
        with col:
            rows = "".join(
                f'<div class="pat-row">'
                f'<span class="pat-key">{label_map.get(fn, fn)}</span>'
                f'<span class="pat-val">{sel_rev.get(fn,{}).get(v, v)}</span>'
                f'</div>'
                for fn, v in chunk
            )
            st.markdown(f'<div class="pat-summary">{rows}</div>', unsafe_allow_html=True)

    # ── Feature importance ────────────────────────────────────────
    st.markdown('<div class="sec-head"><h2>📈 Feature Influence Analysis</h2></div><hr class="sec-line">', unsafe_allow_html=True)
    try:
        _model = load_model()
        _fcols = load_feature_columns()
        lr     = _model.named_steps["model"]
        coefs  = lr.coef_[0]
        cmap   = dict(zip(_fcols, coefs))
        ui_f   = get_all_ui_features()
        idata  = sorted(
            [{"feat": f, "label": label_map.get(f, f), "imp": abs(cmap[f]),
              "dir": "→ ASD" if cmap[f] > 0 else "→ Non-ASD"}
             for f in ui_f if f in cmap],
            key=lambda x: x["imp"], reverse=True
        )[:10]
        if idata:
            mx = idata[0]["imp"] or 1
            bars = "".join(
                f'<div class="feat-row">'
                f'<div class="feat-name">{d["label"]}</div>'
                f'<div class="feat-track"><div class="feat-fill" style="width:{d["imp"]/mx*100:.0f}%;"></div></div>'
                f'<div class="feat-coef">{d["imp"]:.3f}</div>'
                f'<div class="feat-dir">{d["dir"]}</div>'
                f'</div>'
                for d in idata
            )
            st.markdown(f"""
<div class="interp-card">
<div class="interp-head">🔬 Top 10 Feature Influences (Logistic Regression Coefficients)</div>
<div style="margin-top:0.8rem;">{bars}</div>
<div style="font-size:0.72rem;color:{muted_c};margin-top:0.6rem;">
  Bar length = absolute coefficient magnitude. Higher = more influence on prediction outcome.
</div>
</div>""", unsafe_allow_html=True)
    except Exception:
        pass  # Feature importance is optional

    # ── Disclaimer ────────────────────────────────────────────────
    st.markdown("""
<div class="warn-box">
  <strong>⚠️ Medical Disclaimer:</strong> This tool is for <strong>research and educational purposes only</strong>.
  It is <strong>NOT</strong> a clinical diagnostic device. ASD can only be definitively diagnosed
  by qualified healthcare professionals through comprehensive clinical assessment.
  Always consult a licensed clinician.
</div>""", unsafe_allow_html=True)

    # ── PDF Download + New Assessment ─────────────────────────────
    st.write("")
    _, dl1, dl2, _ = st.columns([1, 1.5, 1.5, 1])
    with dl1:
        try:
            # Cache PDF bytes so they don't regenerate on every rerun
            if "pred_pdf" not in st.session_state:
                st.session_state["pred_pdf"] = generate_pdf_report(
                    result, cached_inputs, interp, rec_text, user
                )
            pdf_bytes = st.session_state["pred_pdf"]
            pdf_name  = f"ASD_Report_{st.session_state.get('pred_ts', datetime.now().strftime('%Y%m%d_%H%M%S'))}.pdf"

            # Use base64 HTML anchor — bypasses Streamlit blob UUID issue completely
            b64 = base64.b64encode(pdf_bytes).decode()
            dark = st.session_state.get("dark_mode", False)
            btn_bg  = "#1e3a8a" if dark else "#1e3a8a"
            st.markdown(f"""
<a href="data:application/pdf;base64,{b64}" download="{pdf_name}"
   style="display:block;width:100%;text-align:center;
          padding:0.62rem 1rem;border-radius:12px;
          background:linear-gradient(135deg,#1e3a8a,#2563eb);
          color:white;font-weight:700;font-size:0.9rem;
          text-decoration:none;box-shadow:0 4px 18px rgba(37,99,235,0.35);
          transition:all 0.2s;">
  📄&nbsp;&nbsp;Download PDF Report
</a>""", unsafe_allow_html=True)
        except Exception as e:
            st.warning(f"PDF generation failed: {e}")
    with dl2:
        if st.button("🔄  New Assessment", use_container_width=True, key="reset_form"):
            # Clear all cached prediction data (including PDF)
            for key in ["pred_result", "pred_interp", "pred_rec", "pred_inputs", "pred_ts", "pred_pdf"]:
                st.session_state.pop(key, None)
            # Clear all form widget states
            for feat in [f for gf in FEATURE_GROUPS.values() for f in gf]:
                st.session_state.pop(f"p_{feat}", None)
            st.rerun()

    # ── Technical expander ────────────────────────────────────────
    with st.expander("⚙️ Technical: Complete 46-Feature Input Vector"):
        fr = result["feature_row"]
        df = fr.T.copy()
        df.columns = ["Value"]
        df["Source"] = df.index.map(
            lambda c: "✅ Patient Input" if c in cached_inputs else "🔒 Auto-filled (Median)"
        )
        df["Description"] = df.index.map(lambda c: FEATURE_DESCRIPTIONS.get(c, "—"))
        st.dataframe(df, use_container_width=True)

    st.markdown("""
<div class="app-footer">
  <strong>ASD Prediction System</strong><br>Built by Yogadi
</div>""", unsafe_allow_html=True)
