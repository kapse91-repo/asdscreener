"""Assessment History page — filters, CSV export, expandable records.

Fixes:
- get_css() called once (not repeated in sub-functions)
- Defensive age/confidence access with .get() + fallbacks
- JSON parse error shows friendly message
"""
import json
import csv
import io
import streamlit as st
from helpers.auth import get_user_predictions


def _to_csv(records: list[dict]) -> str:
    """Convert records to CSV string."""
    buf = io.StringIO()
    fields = ["id", "created_at", "prediction", "asd_probability",
              "confidence", "patient_age", "patient_sex"]
    writer = csv.DictWriter(buf, fieldnames=fields, extrasaction="ignore")
    writer.writeheader()
    for r in records:
        row = {k: r.get(k, "") for k in fields}
        row["asd_probability"] = f"{(r.get('asd_probability') or 0)*100:.1f}%"
        row["confidence"]      = f"{(r.get('confidence') or 0)*100:.1f}%"
        sex = str(r.get("patient_sex", ""))
        row["patient_sex"] = "Male" if sex == "1" else ("Female" if sex == "2" else sex)
        writer.writerow(row)
    return buf.getvalue()


def show(user: dict):
    dark = st.session_state.get("dark_mode", False)
    muted_c  = "#64748b" if dark else "#94a3b8"
    sub_c    = "#94a3b8" if dark else "#475569"
    cnt_c    = "#64748b" if dark else "#64748b"

    if st.button("← Back to Dashboard", key="hist_back"):
        st.session_state.page = "dashboard"
        st.rerun()

    st.markdown("""
<div class="page-title">📋 Assessment History</div>
<div class="page-subtitle">All ASD screening assessments you have performed, in reverse chronological order.</div>
<hr class="page-divider">""", unsafe_allow_html=True)

    records = get_user_predictions(user["id"], limit=50)

    if not records:
        st.markdown("""
<div class="info-box">
  No assessments recorded yet. Go to <strong>New Assessment</strong> to run your first prediction.
</div>""", unsafe_allow_html=True)
        if st.button("🔬  Start First Assessment", type="primary"):
            st.session_state.page = "predict"
            st.rerun()
        return

    # ── Stats ──────────────────────────────────────────────────────────
    total  = len(records)
    asd_n  = sum(1 for r in records if r.get("prediction") == "ASD")
    nasd_n = total - asd_n
    conf_vals = [r.get("confidence", 0) for r in records if r.get("confidence") is not None]
    avg_c  = (sum(conf_vals) / len(conf_vals) * 100) if conf_vals else 0

    st.markdown(f"""
<div class="stat-grid">
  <div class="stat-box"><div class="stat-val">{total}</div><div class="stat-lbl">Total Records</div></div>
  <div class="stat-box"><div class="stat-val" style="color:#dc2626;">{asd_n}</div><div class="stat-lbl">ASD Detected</div></div>
  <div class="stat-box"><div class="stat-val" style="color:#059669;">{nasd_n}</div><div class="stat-lbl">Non-ASD</div></div>
  <div class="stat-box"><div class="stat-val">{avg_c:.1f}%</div><div class="stat-lbl">Avg. Confidence</div></div>
</div>""", unsafe_allow_html=True)

    # ── Filter + Sort row ──────────────────────────────────────────────
    st.markdown('<div class="sec-head"><h2>🔍 Filter, Sort &amp; Export</h2></div><hr class="sec-line">', unsafe_allow_html=True)
    f1, f2, f3, f4 = st.columns([1, 1, 1, 1])
    with f1:
        fp = st.selectbox("Prediction", ["All", "ASD", "Non-ASD"])
    with f2:
        fs = st.selectbox("Sex", ["All", "Male", "Female"])
    with f3:
        so = st.selectbox("Sort By", ["Newest First", "Oldest First", "Highest Confidence", "Lowest Confidence"])
    with f4:
        age_min = st.number_input("Min Age", value=0, min_value=0, max_value=100, step=1)

    # Apply filters
    filtered = list(records)
    if fp != "All":
        filtered = [r for r in filtered if r.get("prediction") == fp]
    if fs == "Male":
        filtered = [r for r in filtered if str(r.get("patient_sex","")) == "1"]
    elif fs == "Female":
        filtered = [r for r in filtered if str(r.get("patient_sex","")) == "2"]
    if age_min > 0:
        filtered = [r for r in filtered if (r.get("patient_age") or 0) >= age_min]

    if so == "Oldest First":
        filtered = list(reversed(filtered))
    elif so == "Highest Confidence":
        filtered.sort(key=lambda x: x.get("confidence", 0), reverse=True)
    elif so == "Lowest Confidence":
        filtered.sort(key=lambda x: x.get("confidence", 0))

    # Export + count row
    exp_col, cnt_col = st.columns([1, 3])
    with exp_col:
        if filtered:
            csv_data = _to_csv(filtered)
            st.download_button(
                "📥  Export CSV",
                data=csv_data,
                file_name=f"asd_history_{user.get('username','user')}.csv",
                mime="text/csv",
                use_container_width=True,
            )
    with cnt_col:
        st.markdown(
            f'<div style="font-size:0.82rem;color:{cnt_c};padding-top:0.6rem;">'
            f'Showing <strong>{len(filtered)}</strong> of <strong>{total}</strong> record(s)</div>',
            unsafe_allow_html=True
        )

    if not filtered:
        st.info("No records match the selected filters.")
        return

    st.write("")

    # ── Records ───────────────────────────────────────────────────────
    SEX_MAP = {"1": "Male", "2": "Female"}

    for i, rec in enumerate(filtered):
        is_asd  = rec.get("prediction") == "ASD"
        badge   = "hist-badge-asd" if is_asd else "hist-badge-non"
        bc_val  = "#dc2626" if is_asd else "#059669"
        sex_d   = SEX_MAP.get(str(rec.get("patient_sex","")), "—")
        conf_p  = (rec.get("confidence") or 0) * 100
        asd_p   = (rec.get("asd_probability") or 0) * 100
        age_d   = rec.get("patient_age", "—")
        dt_d    = (rec.get("created_at") or "")[:16]
        pred_d  = rec.get("prediction", "—")

        with st.expander(
            f"#{i+1}  ·  {dt_d}  ·  {pred_d}  ·  "
            f"Age {age_d}  ·  {sex_d}  ·  {conf_p:.1f}% confidence"
        ):
            dd, di = st.columns([1, 2])
            with dd:
                st.markdown(f"""
<div style="border-radius:14px;padding:1.1rem 1.4rem;border:1px solid rgba(128,128,128,0.12);box-shadow:0 2px 8px rgba(0,0,0,0.06);">
  <div style="font-size:1.35rem;font-weight:900;color:{bc_val};margin-bottom:0.45rem;">{pred_d}</div>
  <div style="font-size:0.84rem;color:{sub_c};line-height:1.85;">
    <b>ASD Probability:</b> {asd_p:.1f}%<br>
    <b>Confidence:</b> {conf_p:.1f}%<br>
    <b>Age at Scan:</b> {age_d}<br>
    <b>Sex:</b> {sex_d}<br>
    <b>Recorded:</b> {dt_d}
  </div>
</div>""", unsafe_allow_html=True)
            with di:
                inputs_raw = rec.get("inputs_json", "{}")
                try:
                    inp = json.loads(inputs_raw) if inputs_raw else {}
                    if inp:
                        from helpers.feature_config import FEATURE_GROUPS as FG
                        lmap = {fn: fc["label"] for gf in FG.values() for fn, fc in gf.items()}
                        srev = {fn: {v: k for k, v in fc["options"].items()}
                                for gf in FG.values() for fn, fc in gf.items()
                                if fc["type"] == "select"}
                        rows = "".join(
                            f'<div class="pat-row">'
                            f'<span class="pat-key">{lmap.get(k, k)}</span>'
                            f'<span class="pat-val">{srev.get(k, {}).get(v, v)}</span>'
                            f'</div>'
                            for k, v in inp.items()
                        )
                        st.markdown(
                            f'<div class="pat-summary" style="max-height:250px;overflow-y:auto;">{rows}</div>',
                            unsafe_allow_html=True
                        )
                    else:
                        st.caption("No input detail available for this record.")
                except (json.JSONDecodeError, TypeError):
                    st.caption("Input detail unavailable for this record.")

    st.markdown("""
<div class="app-footer">
  <strong>ASD Prediction System</strong> — Built with Yogadi
</div>""", unsafe_allow_html=True)
