"""
ASD Prediction System — Main router with sidebar + interactive top bar.
Run:  streamlit run app.py

Fixes applied:
- init_db() called only once via session_state flag
- CSS injected once, not on every rerun of sub-pages
- Dark mode toggle is stable (no double-rerun glitch)
- Topbar uses st.session_state to detect click without extra rerun loops
- Page routing uses match-statement equivalent for clarity
"""
import streamlit as st
from helpers.auth import init_db
from helpers.styles import get_css
from helpers.profile_page_helpers import get_initials
from helpers.auth import is_admin as user_is_admin

from pages_ui import auth_page, dashboard_page, predict_page, history_page, profile_page, admin_page

# ── Page config ───────────────────────────────────────────────────────
st.set_page_config(
    page_title="ASD Prediction System",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── DB init — only once per session ───────────────────────────────────
if "db_initialised" not in st.session_state:
    init_db()
    st.session_state.db_initialised = True

# ── Session defaults ──────────────────────────────────────────────────
if "user"      not in st.session_state: st.session_state.user      = None
if "page"      not in st.session_state: st.session_state.page      = "login"
if "dark_mode" not in st.session_state: st.session_state.dark_mode = False

# ── Auth gate ─────────────────────────────────────────────────────────
if st.session_state.user is None:
    auth_page.show()
    st.stop()

# ── CSS (single injection point) ─────────────────────────────────────
st.markdown(get_css(), unsafe_allow_html=True)

# ── Force sidebar always open & remove collapse button ───────────────
st.markdown("""
<style>
[data-testid="stSidebarCollapseButton"],
[data-testid="collapsedControl"] { display:none !important; }
[data-testid="stSidebar"] {
    min-width: 240px !important;
    max-width: 280px !important;
    width: 260px !important;
    transform: none !important;
    visibility: visible !important;
    display: block !important;
}
section[data-testid="stSidebar"][aria-expanded="false"] {
    transform: none !important;
    margin-left: 0 !important;
}
</style>""", unsafe_allow_html=True)

user = st.session_state.user

# ══════════════════════════════════════════════════════════════════════
# TOP ACTION BAR  — profile chip + logout
# ══════════════════════════════════════════════════════════════════════
name_tb   = user.get("full_name") or user.get("username", "User")
inits_tb  = get_initials(name_tb)
av_col_tb = user.get("avatar_color", "#1e3a8a")
role_tb   = (user.get("role") or "").capitalize()
dark_tb   = st.session_state.dark_mode

st.markdown(f"""
<style>
/* ── Top-bar wrapper ────────────────────────── */
div[data-testid="stHorizontalBlock"]:has(button[data-testid="topbar_logout"],
                                         button[data-testid="topbar_profile"]) {{
    position: fixed !important;
    top: 0.45rem !important;
    right: 0.8rem !important;
    z-index: 9999 !important;
    width: auto !important;
    gap: 0.45rem !important;
    background: transparent !important;
}}
button[kind="secondary"][data-testid="topbar_profile"],
div[data-testid="stHorizontalBlock"] button[key="topbar_profile"] {{
    background: {"rgba(17,24,39,0.88)" if dark_tb else "rgba(255,255,255,0.95)"} !important;
    border: 1px solid {"rgba(255,255,255,0.12)" if dark_tb else "rgba(30,58,95,0.13)"} !important;
    border-radius: 50px !important;
    color: {"#e2e8f0" if dark_tb else "#0f172a"} !important;
    font-size: 0.8rem !important; font-weight: 700 !important;
    padding: 0.28rem 1rem !important;
    backdrop-filter: blur(12px) !important;
    box-shadow: 0 2px 14px rgba(0,0,0,0.12) !important;
    min-height: 0 !important; height: auto !important;
    line-height: 1.4 !important; white-space: nowrap !important;
    transition: all 0.2s !important;
}}
button[kind="secondary"][data-testid="topbar_profile"]:hover {{
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 20px rgba(0,0,0,0.18) !important;
    border-color: #2563eb !important;
}}
button[kind="secondary"][data-testid="topbar_logout"],
div[data-testid="stHorizontalBlock"] button[key="topbar_logout"] {{
    background: {"rgba(220,38,38,0.18)" if dark_tb else "rgba(254,226,226,0.9)"} !important;
    border: 1px solid {"rgba(248,113,113,0.35)" if dark_tb else "rgba(239,68,68,0.3)"} !important;
    border-radius: 50px !important;
    color: {"#fca5a5" if dark_tb else "#dc2626"} !important;
    font-size: 0.8rem !important; font-weight: 700 !important;
    padding: 0.28rem 1rem !important;
    backdrop-filter: blur(12px) !important;
    box-shadow: 0 2px 10px rgba(220,38,38,0.1) !important;
    min-height: 0 !important; height: auto !important;
    line-height: 1.4 !important; white-space: nowrap !important;
    min-width: 90px !important; transition: all 0.2s !important;
}}
button[kind="secondary"][data-testid="topbar_logout"]:hover {{
    transform: translateY(-1px) !important;
    background: rgba(220,38,38,0.25) !important;
}}
</style>""", unsafe_allow_html=True)

_spacer, _tb_prof, _tb_lo = st.columns([9, 2.5, 1.5])

with _tb_prof:
    short_name = name_tb[:22]
    if st.button(f"👤  {short_name}", key="topbar_profile", help="View / Edit My Profile",
                 use_container_width=True):
        st.session_state.page = "profile"
        st.rerun()

with _tb_lo:
    if st.button("🚪 Sign Out", key="topbar_logout", help="Sign out",
                 use_container_width=True):
        for k in list(st.session_state.keys()):
            del st.session_state[k]
        st.rerun()

# ══════════════════════════════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════════════════════════════
with st.sidebar:
    # ── Brand ─────────────────────────────────────────────────────────
    st.markdown("""
<div style="text-align:center;padding:1.2rem 0.5rem 0.9rem;">
  <div style="font-size:2.2rem;line-height:1;">🧬</div>
  <div style="font-size:1rem;font-weight:900;color:white;
       letter-spacing:-0.2px;margin-top:0.35rem;">ASD Prediction</div>
  <div style="font-size:0.62rem;color:rgba(255,255,255,0.4);
       letter-spacing:1.6px;text-transform:uppercase;margin-top:0.1rem;">
    AI Screening System
  </div>
</div>""", unsafe_allow_html=True)

    st.markdown('<hr style="border:none;border-top:1px solid rgba(255,255,255,0.1);margin:0 0 0.8rem;">', unsafe_allow_html=True)

    # ── User chip ─────────────────────────────────────────────────────
    name   = user.get("full_name") or user.get("username", "User")
    av_col = user.get("avatar_color", "#1e3a8a")
    inits  = get_initials(name)
    role_d = (user.get("role") or "").capitalize() or "User"

    st.markdown(f"""
<div style="display:flex;align-items:center;gap:0.75rem;
     background:rgba(255,255,255,0.09);border:1px solid rgba(255,255,255,0.1);
     border-radius:14px;padding:0.7rem 1rem;margin-bottom:1rem;">
  <div style="width:38px;height:38px;border-radius:50%;background:{av_col};
       display:flex;align-items:center;justify-content:center;
       font-size:0.88rem;font-weight:900;color:white;flex-shrink:0;
       box-shadow:0 3px 10px rgba(0,0,0,0.25);">{inits}</div>
  <div style="overflow:hidden;">
    <div style="font-size:0.86rem;font-weight:700;color:white;
         white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">{name}</div>
    <div style="font-size:0.67rem;color:rgba(255,255,255,0.45);">{role_d}</div>
  </div>
</div>""", unsafe_allow_html=True)

    # ── NAVIGATION ────────────────────────────────────────────────────
    st.markdown("""
<div style="font-size:0.6rem;font-weight:700;letter-spacing:1.8px;
     color:rgba(255,255,255,0.3);text-transform:uppercase;
     padding:0 0.3rem;margin-bottom:0.3rem;">NAVIGATION</div>""", unsafe_allow_html=True)

    NAV = [
        ("🏠  Dashboard",      "dashboard"),
        ("🔬  New Assessment", "predict"),
        ("📋  History",        "history"),
        ("👤  My Profile",     "profile"),
    ]
    if user_is_admin(user):
        NAV.append(("🛡️  Admin Panel", "admin"))

    cur_page = st.session_state.page
    for label, key in NAV:
        is_active = (cur_page == key)
        btn_clicked = st.button(label, use_container_width=True, key=f"nav_{key}")
        if btn_clicked:
            st.session_state.page = key
            st.rerun()
        if is_active:
            st.markdown(f"""
<style>
div[data-testid="stSidebar"] button[data-testid="nav_{key}"] {{
    background:rgba(255,255,255,0.22) !important;
    border-color:rgba(255,255,255,0.35) !important;
    color:white !important;
}}
</style>""", unsafe_allow_html=True)

    st.markdown('<hr style="border:none;border-top:1px solid rgba(255,255,255,0.1);margin:0.8rem 0;">', unsafe_allow_html=True)

    # ── Dark mode toggle ──────────────────────────────────────────────
    dark = st.session_state.dark_mode
    dm_label = "☀️  Light Mode" if dark else "🌙  Dark Mode"
    if st.button(dm_label, use_container_width=True, key="toggle_dark"):
        st.session_state.dark_mode = not dark
        st.rerun()

    # ── Sign out ──────────────────────────────────────────────────────
    if st.button("🚪  Sign Out", use_container_width=True, key="sidebar_signout"):
        for k in list(st.session_state.keys()):
            del st.session_state[k]
        st.rerun()

    # ── Sidebar footer ────────────────────────────────────────────────
    st.markdown("""
<div style="text-align:center;font-size:0.6rem;color:rgba(255,255,255,0.2);
     margin-top:1.6rem;line-height:1.7;padding:0 0.4rem;">
  Built by Yogadi<br>
  UCLA ABIDE · 46 Features · LR Model
</div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════
# PAGE ROUTING
# ══════════════════════════════════════════════════════════════════════
page = st.session_state.page

if   page == "dashboard": dashboard_page.show(user)
elif page == "predict":   predict_page.show(user)
elif page == "history":   history_page.show(user)
elif page == "profile":   profile_page.show(user)
elif page == "admin":     admin_page.show(user)
else:
    st.session_state.page = "dashboard"
    st.rerun()
