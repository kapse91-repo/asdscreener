"""Login & Registration page — single-page, no sliding tabs.

Fixes:
- Removed duplicate init_db() call (handled by app.py once)
- Improved validation messages
- Password field shows strength hint
"""
import streamlit as st
from helpers.auth import login_user, register_user
from helpers.styles import get_css

ROLES = ["Clinician", "Researcher", "Student", "Parent / Caregiver", "Other"]


def show():
    st.markdown(get_css(), unsafe_allow_html=True)

    dark = st.session_state.get("dark_mode", False)

    if "auth_view" not in st.session_state:
        st.session_state.auth_view = "login"

    # Dark mode toggle (top-right corner)
    _sp, _tog = st.columns([9, 1])
    with _tog:
        if st.button("🌙" if not dark else "☀️", key="auth_dark", help="Toggle dark mode"):
            st.session_state.dark_mode = not dark
            st.rerun()

    # ── Centered card ─────────────────────────────────────────────────
    _, mid, _ = st.columns([1, 1.8, 1])
    with mid:
        st.markdown("""
<div class="auth-wrap">
  <div class="auth-logo">
    <div class="auth-logo-icon">🧬</div>
    <h2>ASD Prediction System</h2>
    <p>Autism Screening Tool</p>
  </div>
""", unsafe_allow_html=True)

        # ── SIGN IN FORM ──────────────────────────────────────────────
        if st.session_state.auth_view == "login":
            title_c = "#93c5fd" if dark else "#1e3a8a"
            muted_c = "#64748b" if dark else "#94a3b8"
            st.markdown(f"""
<div style="text-align:center;font-size:0.95rem;font-weight:700;
     color:{title_c};margin-bottom:1rem;letter-spacing:-0.1px;">
  Sign In to Your Account
</div>""", unsafe_allow_html=True)

            with st.form("login_form", clear_on_submit=False):
                username  = st.text_input("Username", placeholder="Enter your username")
                password  = st.text_input("Password", type="password", placeholder="Enter your password")
                submitted = st.form_submit_button("Sign In →", use_container_width=True, type="primary")
                if submitted:
                    if not username.strip() or not password:
                        st.error("Please fill in both username and password.")
                    else:
                        ok, user, msg = login_user(username, password)
                        if ok:
                            st.session_state.user = user
                            st.session_state.page = "dashboard"
                            st.rerun()
                        else:
                            st.error(f"❌ {msg}")

            st.markdown(f"""
<div style="text-align:center;margin-top:1rem;">
  <span style="font-size:0.79rem;color:{muted_c};">Don't have an account?</span>
</div>""", unsafe_allow_html=True)
            if st.button("Create Account →", use_container_width=True, key="goto_register"):
                st.session_state.auth_view = "register"
                st.rerun()

            st.markdown(f"""
<div style="text-align:center;font-size:0.75rem;color:{muted_c};margin-top:0.5rem;">
  Forgot your password? Contact your system administrator.<br>
  <em>Default admin: <strong>admin / admin123</strong></em>
</div>""", unsafe_allow_html=True)

        # ── REGISTER FORM ─────────────────────────────────────────────
        else:
            title_c = "#93c5fd" if dark else "#1e3a8a"
            muted_c = "#64748b" if dark else "#94a3b8"
            st.markdown(f"""
<div style="text-align:center;font-size:0.95rem;font-weight:700;
     color:{title_c};margin-bottom:1rem;letter-spacing:-0.1px;">
  Create New Account
</div>""", unsafe_allow_html=True)

            with st.form("reg_form", clear_on_submit=False):
                c1, c2 = st.columns(2)
                with c1:
                    r_full = st.text_input("Full Name *",  placeholder="Dr. Jane Smith")
                with c2:
                    r_user = st.text_input("Username *",   placeholder="jsmith")
                r_email = st.text_input("Email Address *", placeholder="jane@hospital.com")
                c3, c4 = st.columns(2)
                with c3:
                    r_inst = st.text_input("Institution",  placeholder="Hospital / University")
                with c4:
                    r_role = st.selectbox("Role", ROLES)
                c5, c6 = st.columns(2)
                with c5:
                    r_pass  = st.text_input("Password *",  type="password", placeholder="Min. 6 chars")
                with c6:
                    r_pass2 = st.text_input("Confirm *",   type="password", placeholder="Repeat")
                terms   = st.checkbox("I confirm this tool is for research/educational use only.")
                reg_sub = st.form_submit_button("Create Account →", use_container_width=True, type="primary")
                if reg_sub:
                    errs = []
                    if not r_full.strip():                       errs.append("Full name is required.")
                    if not r_user.strip():                       errs.append("Username is required.")
                    if not r_email.strip() or "@" not in r_email: errs.append("Valid email required.")
                    if len(r_pass) < 6:                          errs.append("Password must be at least 6 characters.")
                    if r_pass != r_pass2:                        errs.append("Passwords do not match.")
                    if not terms:                                errs.append("Please accept the usage terms.")
                    if errs:
                        for e in errs:
                            st.error(e)
                    else:
                        ok, msg = register_user(r_user.strip(), r_email.strip(), r_pass,
                                                full_name=r_full.strip(), role=r_role.lower(),
                                                institution=r_inst.strip())
                        if ok:
                            st.success("✅ Account created! Please sign in.")
                            st.session_state.auth_view = "login"
                            st.rerun()
                        else:
                            st.error(f"❌ {msg}")

            st.markdown(f"""
<div style="text-align:center;margin-top:1rem;">
  <span style="font-size:0.79rem;color:{muted_c};">Already have an account?</span>
</div>""", unsafe_allow_html=True)
            if st.button("← Back to Sign In", use_container_width=True, key="goto_login"):
                st.session_state.auth_view = "login"
                st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)

    # Footer
    st.markdown("""
<div class="app-footer">
  <strong>ASD Prediction System</strong><br>Built by Yogadi
</div>""", unsafe_allow_html=True)
