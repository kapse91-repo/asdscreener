"""
Profile page — editable, avatar, change password, back nav, sign out.
Fix: removed local _change_password (moved to auth.py), cleaner forms.
"""
import streamlit as st
from helpers.auth import update_profile, get_user, change_password
from helpers.profile_page_helpers import get_initials, COLOR_MAP

ROLES = ["Clinician", "Researcher", "Student", "Parent / Caregiver", "Other"]


def show(user: dict):
    dark = st.session_state.get("dark_mode", False)
    hr_c = "rgba(255,255,255,0.1)" if dark else "#e2e8f0"

    if st.button("← Back to Dashboard", key="prof_back"):
        st.session_state.page = "dashboard"
        st.rerun()

    fresh  = get_user(user["id"]) or user
    name   = fresh.get("full_name") or fresh.get("username", "User")
    role   = fresh.get("role", "").capitalize()
    inst   = fresh.get("institution") or "—"
    email  = fresh.get("email", "—")
    joined = (fresh.get("created_at") or "—")[:10]
    last   = (fresh.get("last_login") or "—")[:16]
    av_col = fresh.get("avatar_color", "#1e3a8a")
    inits  = get_initials(name)

    st.markdown("""
<div class="page-title">👤 My Profile</div>
<div class="page-subtitle">Manage your professional details and account settings.</div>
<hr class="page-divider">""", unsafe_allow_html=True)

    # ── Profile header ────────────────────────────────────────────────
    st.markdown(f"""
<div class="profile-header">
  <div class="avatar" style="background:{av_col};">{inits}</div>
  <div>
    <div class="profile-name">{name}</div>
    <div class="profile-role">🏷️ {role} &nbsp;|&nbsp; 🏛️ {inst}</div>
    <div class="profile-meta">
      ✉️ {email} &nbsp;&nbsp;
      📅 Joined {joined} &nbsp;&nbsp;
      🕒 Last login: {last}
    </div>
  </div>
</div>""", unsafe_allow_html=True)

    # ── Tabs: Edit Profile | Change Password | Account Info ───────────
    tab_edit, tab_pw, tab_acct = st.tabs(["✏️  Edit Profile", "🔑  Change Password", "🔐  Account Info"])

    # ── TAB 1: Edit Profile ───────────────────────────────────────────
    with tab_edit:
        with st.form("profile_form"):
            c1, c2 = st.columns(2)
            with c1:
                f_name  = st.text_input("Full Name",      value=fresh.get("full_name",""),   placeholder="Dr. Jane Smith")
                f_phone = st.text_input("Phone/Contact",  value=fresh.get("phone",""),       placeholder="+91 98765 43210")
            with c2:
                f_inst  = st.text_input("Institution",    value=fresh.get("institution",""), placeholder="Hospital / University")
                color_names = list(COLOR_MAP.keys())
                cur_color   = fresh.get("avatar_color", "#1e3a8a")
                cur_name    = next((k for k, v in COLOR_MAP.items() if v == cur_color), color_names[0])
                f_color = st.selectbox("Avatar Color", color_names, index=color_names.index(cur_name))

            role_caps = [r.capitalize() if r else "" for r in ROLES]
            cur_role  = role if role in role_caps else role_caps[0]
            f_role    = st.selectbox("Your Role", role_caps,
                                     index=role_caps.index(cur_role) if cur_role in role_caps else 0)

            f_bio = st.text_area("Short Bio", value=fresh.get("bio",""),
                                 placeholder="Brief professional description...",
                                 max_chars=300, height=85)

            saved = st.form_submit_button("💾  Save Changes", use_container_width=True, type="primary")

        if saved:
            if not f_name.strip():
                st.error("❌ Full name cannot be empty.")
            else:
                ok, msg = update_profile(
                    user_id=user["id"], full_name=f_name, institution=f_inst,
                    phone=f_phone, bio=f_bio, avatar_color=COLOR_MAP[f_color],
                )
                if ok:
                    updated = get_user(user["id"])
                    if updated:
                        st.session_state.user = updated
                    st.success(f"✅ {msg}")
                    st.rerun()
                else:
                    st.error(f"❌ {msg}")

    # ── TAB 2: Change Password ────────────────────────────────────────
    with tab_pw:
        st.markdown("""
<div class="info-box" style="margin-top:0.5rem;">
  For security, enter your current password before setting a new one.
  Password must be at least 6 characters long.
</div>""", unsafe_allow_html=True)

        with st.form("pw_form"):
            old_pw  = st.text_input("Current Password", type="password", placeholder="Enter current password")
            new_pw  = st.text_input("New Password",     type="password", placeholder="Minimum 6 characters")
            conf_pw = st.text_input("Confirm New Password", type="password", placeholder="Repeat new password")
            pw_sub  = st.form_submit_button("🔑  Update Password", use_container_width=True, type="primary")

        if pw_sub:
            errs = []
            if not old_pw:                  errs.append("Current password is required.")
            if len(new_pw) < 6:             errs.append("New password must be at least 6 characters.")
            if new_pw != conf_pw:           errs.append("New passwords do not match.")
            if old_pw and new_pw == old_pw: errs.append("New password must differ from the current one.")
            if errs:
                for e in errs:
                    st.error(e)
            else:
                ok, msg = change_password(user["id"], old_pw, new_pw)
                if ok:
                    st.success(f"✅ {msg} Please sign in again.")
                    import time
                    time.sleep(1.5)
                    for k in list(st.session_state.keys()):
                        del st.session_state[k]
                    st.rerun()
                else:
                    st.error(f"❌ {msg}")

    # ── TAB 3: Account Info ───────────────────────────────────────────
    with tab_acct:
        st.write("")
        ai1, ai2 = st.columns(2)
        with ai1:
            st.markdown(f"""
<div class="card">
  <div class="interp-head">Account Details</div>
  <div class="interp-body">
    <b>Username:</b> {fresh.get('username','—')}<br>
    <b>Email:</b> {email}<br>
    <b>Role:</b> {role}<br>
    <b>Account Created:</b> {joined}
  </div>
</div>""", unsafe_allow_html=True)
        with ai2:
            st.markdown(f"""
<div class="card">
  <div class="interp-head">Activity Summary</div>
  <div class="interp-body">
    <b>Last Login:</b> {last}<br>
    <b>Institution:</b> {inst}<br>
    <b>Phone:</b> {fresh.get('phone','—') or '—'}<br>
    <b>Bio:</b> {fresh.get('bio','(not set)') or '(not set)'}
  </div>
</div>""", unsafe_allow_html=True)

        st.markdown("""
<div class="warn-box">
  <b>Data Notice:</b> All assessment data is stored locally in an SQLite database
  on this machine. No data is transmitted externally. For research use only.
</div>""", unsafe_allow_html=True)

    # ── Sign out (centered) ───────────────────────────────────────────
    st.markdown(f'<hr style="border:none;border-top:1px solid {hr_c};margin:1.2rem 0 0.8rem;">', unsafe_allow_html=True)
    _sl, _sc, _sr = st.columns([2, 2, 2])
    with _sc:
        if st.button("🚪  Sign Out", type="secondary", key="sign_out_btn", use_container_width=True):
            for k in list(st.session_state.keys()):
                del st.session_state[k]
            st.rerun()

    st.markdown("""
<div class="app-footer">
  <strong>ASD Prediction System</strong> — Built with Yogadi
</div>""", unsafe_allow_html=True)
