"""Dashboard — personalized home page, compact layout."""
import streamlit as st
from helpers.auth import get_stats, get_user_predictions, get_system_stats
from helpers.auth import is_admin as check_admin


def show(user: dict):
    dark = st.session_state.get("dark_mode", False)
    muted_c = "#64748b" if dark else "#94a3b8"

    name  = user.get("full_name") or user.get("username", "User")
    role  = (user.get("role") or "").lower()
    clean_name = name.strip()
    if clean_name.lower().startswith("dr."):
        clean_name = clean_name[3:].strip()
    elif clean_name.lower().startswith("dr "):
        clean_name = clean_name[3:].strip()
    prefix = "Dr." if role in ("clinician", "admin", "researcher") else ""
    disp   = f"{prefix} {clean_name}".strip()

    is_adm = check_admin(user)

    # ── Hero ──────────────────────────────────────────────────────────
    st.markdown(f"""
<div class="hero">
  <div class="hero-badge">🧬 Clinical Analytics Dashboard</div>
  <h1>Welcome, {disp}</h1>
</div>""", unsafe_allow_html=True)

    # ── Stats (own stats for regular user, system-wide for admin) ─────
    if is_adm:
        s_all = get_system_stats()
        asd_c    = f'<div class="stat-val" style="color:#dc2626;">{s_all["asd_preds"]}</div>'
        nonasd_c = f'<div class="stat-val" style="color:#16a34a;">{s_all["nonasd_preds"]}</div>'
        st.markdown(f"""
<div class="stat-grid">
  <div class="stat-box"><div class="stat-val">{s_all['total_users']}</div><div class="stat-lbl">Total Users</div></div>
  <div class="stat-box"><div class="stat-val">{s_all['total_preds']}</div><div class="stat-lbl">Total Assessments</div></div>
  <div class="stat-box">{asd_c}<div class="stat-lbl">ASD Predicted</div></div>
  <div class="stat-box">{nonasd_c}<div class="stat-lbl">Non-ASD Predicted</div></div>
  <div class="stat-box"><div class="stat-val">{s_all['avg_confidence']}%</div><div class="stat-lbl">Avg. Confidence</div></div>
  <div class="stat-box"><div class="stat-val" style="color:#7c3aed;">{s_all['today_preds']}</div><div class="stat-lbl">Today's Assessments</div></div>
</div>""", unsafe_allow_html=True)
    else:
        s = get_stats(user["id"])
        asd_c    = f'<div class="stat-val" style="color:#dc2626;">{s["asd_count"]}</div>'
        nonasd_c = f'<div class="stat-val" style="color:#16a34a;">{s["nonasd_count"]}</div>'
        st.markdown(f"""
<div class="stat-grid">
  <div class="stat-box"><div class="stat-val">{s['total']}</div><div class="stat-lbl">My Assessments</div></div>
  <div class="stat-box">{asd_c}<div class="stat-lbl">ASD Predicted</div></div>
  <div class="stat-box">{nonasd_c}<div class="stat-lbl">Non-ASD Predicted</div></div>
  <div class="stat-box"><div class="stat-val">{s['avg_confidence']}%</div><div class="stat-lbl">Avg. Confidence</div></div>
</div>""", unsafe_allow_html=True)

    # ── Quick actions ─────────────────────────────────────────────────
    st.markdown('<div class="sec-head"><h2>🚀 Quick Actions</h2></div><hr class="sec-line">', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3, gap="medium")

    with c1:
        st.markdown("""
<div class="qa-card" style="border-top:3px solid #1565a0;">
  <div class="qa-icon">🔬</div>
  <div class="qa-title">New Assessment</div>
  <div class="qa-desc">Run an AI-assisted ASD prediction using clinical and behavioral scores.</div>
</div>""", unsafe_allow_html=True)
        if st.button("Start Assessment →", use_container_width=True, key="dash_predict"):
            st.session_state.page = "predict"; st.rerun()

    with c2:
        st.markdown("""
<div class="qa-card" style="border-top:3px solid #7c3aed;">
  <div class="qa-icon">📋</div>
  <div class="qa-title">Assessment History</div>
  <div class="qa-desc">Review past patient records, filter results, and expand detailed reports.</div>
</div>""", unsafe_allow_html=True)
        if st.button("View History →", use_container_width=True, key="dash_hist"):
            st.session_state.page = "history"; st.rerun()

    with c3:
        st.markdown("""
<div class="qa-card" style="border-top:3px solid #0891b2;">
  <div class="qa-icon">👤</div>
  <div class="qa-title">My Profile</div>
  <div class="qa-desc">Update your professional details, institution, role, and avatar.</div>
</div>""", unsafe_allow_html=True)
        if st.button("Edit Profile →", use_container_width=True, key="dash_profile"):
            st.session_state.page = "profile"; st.rerun()

    # ── Recent assessments ────────────────────────────────────────────
    st.markdown('<div class="sec-head"><h2>🕒 Recent Assessments</h2></div><hr class="sec-line">', unsafe_allow_html=True)

    # Admin: show all recent across all users; regular user: own only
    if is_adm:
        from helpers.auth import get_all_predictions
        recent_raw = get_all_predictions(limit=5)
        # Normalize field names for unified rendering
        recent = []
        for r in recent_raw:
            recent.append({
                "prediction":  r["prediction"],
                "patient_age": r.get("patient_age"),
                "patient_sex": r.get("patient_sex"),
                "confidence":  r.get("confidence", 0),
                "created_at":  r.get("created_at", ""),
                "_user":       r.get("username", ""),
            })
    else:
        recent_raw = get_user_predictions(user["id"], limit=5)
        recent = [{**r, "_user": None} for r in recent_raw]

    if not recent:
        st.markdown("""
<div class="info-box">
  No assessments yet. Click <strong>Start Assessment</strong> above to run your first prediction.
</div>""", unsafe_allow_html=True)
    else:
        sex_map = {"1": "Male", "2": "Female"}
        for rec in recent:
            is_asd  = rec["prediction"] == "ASD"
            badge   = "hist-badge-asd" if is_asd else "hist-badge-non"
            sex_d   = sex_map.get(str(rec.get("patient_sex", "")), "—")
            conf_p  = rec["confidence"] * 100
            user_lbl = f" &nbsp;|&nbsp; By: <strong>{rec['_user']}</strong>" if is_adm and rec.get("_user") else ""
            st.markdown(f"""
<div class="hist-row" style="display:flex;align-items:center;gap:1rem;">
  <span class="{badge}">{rec['prediction']}</span>
  <span style="font-size:0.84rem;flex:1;">
    Age: <strong>{rec.get('patient_age','—')}</strong> &nbsp;|&nbsp;
    Sex: <strong>{sex_d}</strong> &nbsp;|&nbsp;
    Confidence: <strong>{conf_p:.1f}%</strong>{user_lbl}
  </span>
  <span style="font-size:0.73rem;color:{muted_c};">{rec['created_at'][:16]}</span>
</div>""", unsafe_allow_html=True)

    st.markdown("""
<div class="app-footer">
  <strong>ASD Prediction System</strong><br>Built by Yogadi
</div>""", unsafe_allow_html=True)
