"""
Global CSS design system — Premium Light + Dark mode.
Inject via: st.markdown(get_css(), unsafe_allow_html=True)

Color Palette (Light):
  Primary:    #1e3a5f  (Deep Indigo Navy)
  Accent:     #2563eb  (Vivid Royal Blue)
  Highlight:  #06b6d4  (Teal Cyan)
  Success:    #059669  (Emerald)
  Danger:     #dc2626  (Crimson)
  Surface:    #f8fafd  (Ice Blue White)
  Card:       #ffffff
  Sidebar:    #0f1f3d → #1e3a6e → #2563eb

Color Palette (Dark):
  Primary:    #e2e8f0
  Accent:     #3b82f6
  Surface:    #0b1120
  Card:       #111827
  Sidebar:    #060d1a → #0f1f3d → #1a3052
"""
import streamlit as st


def get_css() -> str:
    dark = st.session_state.get("dark_mode", False)

    if dark:
        # ── Dark Palette ──────────────────────────────────────────────
        bg_main      = "#0b1120"
        bg_card      = "#111827"
        bg_card2     = "#1a2235"
        bg_sidebar   = "linear-gradient(180deg,#060d1a 0%,#0f1f3d 55%,#1a3052 100%)"
        text_main    = "#e2e8f0"
        text_sub     = "#94a3b8"
        text_muted   = "#64748b"
        border_col   = "rgba(255,255,255,0.06)"
        border_col2  = "rgba(255,255,255,0.1)"
        input_bg     = "#1a2235"
        input_bdr    = "#2d4060"
        input_focus  = "#3b82f6"
        card_shadow  = "0 4px 28px rgba(0,0,0,0.45)"
        card_hover   = "0 10px 40px rgba(0,0,0,0.5)"
        stat_bg      = "#111827"
        info_bg      = "#0a1e38"
        info_bdr     = "#1d4ed8"
        info_txt     = "#93c5fd"
        warn_bg      = "#130e00"
        warn_bdr     = "#b45309"
        warn_txt     = "#fbbf24"
        hr_col       = "rgba(255,255,255,0.07)"
        hero_grd     = "linear-gradient(135deg,#060d1a 0%,#0f2851 45%,#1e4080 100%)"
        hero_glow    = "rgba(59,130,246,0.15)"
        histrow_bg   = "#111827"
        auth_bg      = "#111827"
        auth_shadow  = "0 24px 60px rgba(0,0,0,0.5)"
        pat_bdr      = "rgba(255,255,255,0.04)"
        nav_hover    = "rgba(255,255,255,0.09)"
        accent       = "#3b82f6"
        accent2      = "#06b6d4"
        primary_grd  = "linear-gradient(135deg,#1e3a8a 0%,#2563eb 100%)"
        chip_bg      = "rgba(255,255,255,0.08)"
        chip_border  = "rgba(255,255,255,0.1)"
        sec_color    = "#60a5fa"
        title_color  = "#93c5fd"
        feat_fill    = "linear-gradient(90deg,#06b6d4,#3b82f6)"
        qa_border_1  = "#3b82f6"
        qa_border_2  = "#8b5cf6"
        qa_border_3  = "#06b6d4"
        badge_asd_bg = "#3d1515"
        badge_asd_fg = "#f87171"
        badge_non_bg = "#0f2d1f"
        badge_non_fg = "#34d399"
    else:
        # ── Light Palette ─────────────────────────────────────────────
        bg_main      = "#f0f5fb"
        bg_card      = "#ffffff"
        bg_card2     = "#f4f7fb"
        bg_sidebar   = "linear-gradient(180deg,#0f1f3d 0%,#1e3a6e 50%,#2563eb 100%)"
        text_main    = "#0f172a"
        text_sub     = "#475569"
        text_muted   = "#94a3b8"
        border_col   = "rgba(30,58,95,0.07)"
        border_col2  = "rgba(30,58,95,0.14)"
        input_bg     = "#ffffff"
        input_bdr    = "#cbd5e1"
        input_focus  = "#2563eb"
        card_shadow  = "0 2px 18px rgba(15,31,63,0.06)"
        card_hover   = "0 8px 36px rgba(15,31,63,0.12)"
        stat_bg      = "#ffffff"
        info_bg      = "#eff6ff"
        info_bdr     = "#3b82f6"
        info_txt     = "#1e3a8a"
        warn_bg      = "#fffbeb"
        warn_bdr     = "#f59e0b"
        warn_txt     = "#92400e"
        hr_col       = "rgba(15,31,63,0.08)"
        hero_grd     = "linear-gradient(135deg,#0f2851 0%,#1e4da0 40%,#2563eb 80%,#0ea5e9 100%)"
        hero_glow    = "rgba(37,99,235,0.08)"
        histrow_bg   = "#ffffff"
        auth_bg      = "#ffffff"
        auth_shadow  = "0 16px 56px rgba(15,31,63,0.12)"
        pat_bdr      = "rgba(15,31,63,0.05)"
        nav_hover    = "rgba(255,255,255,0.12)"
        accent       = "#2563eb"
        accent2      = "#06b6d4"
        primary_grd  = "linear-gradient(135deg,#1e3a8a 0%,#2563eb 100%)"
        chip_bg      = "rgba(255,255,255,0.1)"
        chip_border  = "rgba(255,255,255,0.15)"
        sec_color    = "#1e3a8a"
        title_color  = "#1e3a8a"
        feat_fill    = "linear-gradient(90deg,#06b6d4,#2563eb)"
        qa_border_1  = "#2563eb"
        qa_border_2  = "#7c3aed"
        qa_border_3  = "#06b6d4"
        badge_asd_bg = "#fef2f2"
        badge_asd_fg = "#dc2626"
        badge_non_bg = "#ecfdf5"
        badge_non_fg = "#059669"

    return f"""
<style>
/* ═══════════════════════════════════════════════════════════
   ASD PREDICTION SYSTEM — Global Design System
   ═══════════════════════════════════════════════════════ */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

/* ── Reset ─────────────────────────────────────────────── */
html, body, [class*="css"] {{
    font-family:'Inter', sans-serif !important;
    transition: background 0.35s, color 0.35s;
}}

/* ── App background ─────────────────────────────────────── */
.stApp {{
    background:{bg_main} !important;
    color:{text_main} !important;
}}

/* ── Hide ALL Streamlit chrome ──────────────────────────── */
#MainMenu, footer, header {{ visibility:hidden !important; }}
.stDeployButton,
[data-testid="stToolbar"],
[data-testid="stDecoration"],
[data-testid="stSidebarNav"] {{ display:none !important; }}

/* ── REMOVE "Press Enter to submit form" text ───────────── */
[data-testid="InputInstructions"],
.stNumberInput [data-testid="InputInstructions"],
.stTextInput [data-testid="InputInstructions"] {{
    display: none !important;
    visibility: hidden !important;
    height: 0 !important;
    overflow: hidden !important;
}}

/* ── Remove Streamlit top padding (default ~6rem gap) ────── */
.block-container {{
    padding-top: 0.8rem !important;
    padding-bottom: 0.8rem !important;
}}
[data-testid="stAppViewBlockContainer"] {{
    padding-top: 0.8rem !important;
}}

/* ── Global text ─────────────────────────────────────────── */
p, span, div, label, h1, h2, h3, h4, h5 {{ color:{text_main}; }}
.stMarkdown p {{ color:{text_main}; }}

/* ═══════════════════════════════════════════════════════════
   SIDEBAR
   ═══════════════════════════════════════════════════════ */
[data-testid="stSidebar"] {{
    background:{bg_sidebar} !important;
    border-right:none !important;
    box-shadow:6px 0 40px rgba(0,0,0,0.3);
}}
[data-testid="stSidebar"] * {{ transition: all 0.2s; }}
[data-testid="stSidebar"] button {{
    background:rgba(255,255,255,0.07) !important;
    color:#dbeafe !important;
    border:1px solid rgba(255,255,255,0.08) !important;
    border-radius:12px !important;
    font-weight:600 !important;
    font-size:0.87rem !important;
    padding:0.58rem 1rem !important;
    text-align:left !important;
    transition:all 0.22s !important;
    margin-bottom:3px !important;
    letter-spacing:0.01em !important;
}}
[data-testid="stSidebar"] button:hover {{
    background:{nav_hover} !important;
    border-color:rgba(255,255,255,0.2) !important;
    transform:translateX(3px) !important;
    box-shadow:0 4px 16px rgba(0,0,0,0.2) !important;
}}

/* ═══════════════════════════════════════════════════════════
   FORM INPUTS
   ═══════════════════════════════════════════════════════ */
.stTextInput input,
.stNumberInput input,
.stTextArea textarea {{
    background:{input_bg} !important;
    border:1.5px solid {input_bdr} !important;
    border-radius:10px !important;
    color:{text_main} !important;
    font-size:0.9rem !important;
    transition:border-color 0.25s, box-shadow 0.25s !important;
    padding:0.55rem 0.85rem !important;
}}
.stTextInput input:focus,
.stNumberInput input:focus,
.stTextArea textarea:focus {{
    border-color:{input_focus} !important;
    box-shadow:0 0 0 3px rgba(37,99,235,0.14) !important;
    outline:none !important;
}}
.stTextInput input::placeholder,
.stTextArea textarea::placeholder {{
    color:{text_muted} !important;
    font-style:italic;
}}
.stSelectbox [data-baseweb="select"] > div {{
    background:{input_bg} !important;
    border:1.5px solid {input_bdr} !important;
    border-radius:10px !important;
    color:{text_main} !important;
}}
.stSelectbox [data-baseweb="select"] > div:focus-within {{
    border-color:{input_focus} !important;
    box-shadow:0 0 0 3px rgba(37,99,235,0.14) !important;
}}

/* ═══════════════════════════════════════════════════════════
   BUTTONS
   ═══════════════════════════════════════════════════════ */
.stButton > button[kind="primary"] {{
    background:{primary_grd} !important;
    color:#fff !important; border:none !important;
    border-radius:12px !important; font-weight:700 !important;
    font-size:0.92rem !important; letter-spacing:0.01em !important;
    box-shadow:0 4px 20px rgba(37,99,235,0.35) !important;
    transition:all 0.28s !important;
    padding:0.68rem 1.5rem !important;
}}
.stButton > button[kind="primary"]:hover {{
    transform:translateY(-2px) !important;
    box-shadow:0 10px 30px rgba(37,99,235,0.45) !important;
}}
.stButton > button {{
    border-radius:12px !important;
    font-weight:600 !important;
    transition:all 0.22s !important;
}}
.stButton > button[kind="secondary"] {{
    background:{bg_card2} !important;
    color:{text_sub} !important;
    border:1.5px solid {input_bdr} !important;
    border-radius:12px !important;
}}
.stButton > button[kind="secondary"]:hover {{
    border-color:{accent} !important;
    color:{accent} !important;
    transform:translateY(-1px) !important;
}}
.stDownloadButton > button {{
    background:linear-gradient(135deg,#059669 0%,#047857 100%) !important;
    color:white !important; border:none !important;
    border-radius:12px !important; font-weight:700 !important;
    box-shadow:0 4px 18px rgba(5,150,105,0.3) !important;
    transition:all 0.28s !important;
}}
.stDownloadButton > button:hover {{
    transform:translateY(-2px) !important;
    box-shadow:0 8px 26px rgba(5,150,105,0.4) !important;
}}

/* ═══════════════════════════════════════════════════════════
   TABS
   ═══════════════════════════════════════════════════════ */
.stTabs [data-baseweb="tab-list"] {{
    background:{bg_card2} !important;
    border-radius:12px !important; padding:4px !important;
    gap:4px !important; border:1px solid {border_col} !important;
}}
.stTabs [data-baseweb="tab"] {{
    background:transparent !important;
    color:{text_sub} !important;
    border-radius:9px !important;
    font-weight:600 !important; font-size:0.87rem !important;
    border:none !important; transition:all 0.22s !important;
}}
.stTabs [data-baseweb="tab"]:hover {{
    color:{accent} !important;
}}
.stTabs [aria-selected="true"] {{
    background:{bg_card} !important;
    color:{accent} !important;
    box-shadow:0 2px 10px rgba(37,99,235,0.12) !important;
}}

/* ═══════════════════════════════════════════════════════════
   EXPANDERS
   ═══════════════════════════════════════════════════════ */
.stExpander {{
    background:{bg_card} !important;
    border:1px solid {border_col} !important;
    border-radius:14px !important;
    box-shadow:{card_shadow} !important;
    overflow:hidden !important;
}}
.stExpander summary {{
    color:{text_main} !important;
    font-weight:600 !important;
    font-size:0.9rem !important;
    padding:0.9rem 1.2rem !important;
}}
.stExpander summary:hover {{ color:{accent} !important; }}

/* ── Spinner ─────────────────────────────────────────────── */
.stSpinner > div {{ border-top-color:{accent} !important; }}

/* ── Alerts ──────────────────────────────────────────────── */
.stAlert {{ border-radius:12px !important; }}

/* ═══════════════════════════════════════════════════════════
   HERO BANNER
   ═══════════════════════════════════════════════════════ */
.hero {{
    background:{hero_grd};
    border-radius:18px; padding:1.5rem 2rem;
    color:white; position:relative; overflow:hidden;
    box-shadow:0 12px 36px rgba(15,40,81,0.22);
    margin-bottom:1.1rem;
}}
.hero::before {{
    content:''; position:absolute;
    width:500px; height:500px;
    background:radial-gradient(circle,rgba(255,255,255,0.07) 0%,transparent 65%);
    border-radius:50%; top:-60%; right:-12%; pointer-events:none;
}}
.hero::after {{
    content:''; position:absolute;
    width:200px; height:200px;
    background:radial-gradient(circle,rgba(6,182,212,0.12) 0%,transparent 70%);
    border-radius:50%; bottom:-20%; left:5%; pointer-events:none;
}}
.hero-badge {{
    display:inline-block;
    background:rgba(255,255,255,0.13);
    border:1px solid rgba(255,255,255,0.22);
    font-size:0.66rem; font-weight:700;
    letter-spacing:2.5px; text-transform:uppercase;
    padding:0.38rem 1.1rem; border-radius:50px;
    margin-bottom:1.1rem; color:#bae6fd;
    backdrop-filter:blur(4px);
}}
.hero h1 {{
    font-size:2rem; font-weight:900; margin:0 0 0.5rem 0;
    line-height:1.1; letter-spacing:-0.5px; color:white !important;
    text-shadow:0 2px 16px rgba(0,0,0,0.15);
}}
.hero p {{
    font-size:0.97rem; opacity:0.87; line-height:1.68;
    margin:0; color:rgba(255,255,255,0.9) !important;
    max-width:680px;
}}

/* ═══════════════════════════════════════════════════════════
   CARDS
   ═══════════════════════════════════════════════════════ */
.card {{
    background:{bg_card}; border-radius:18px;
    padding:1.6rem 1.8rem; border:1px solid {border_col};
    box-shadow:{card_shadow}; margin-bottom:1.1rem;
    transition:box-shadow 0.28s, transform 0.28s;
}}
.card:hover {{ box-shadow:{card_hover}; transform:translateY(-2px); }}

/* ── Page header ─────────────────────────────────────────── */
.page-title {{
    font-size:1.55rem; font-weight:800; color:{title_color};
    margin:0 0 0.22rem 0;
}}
.page-subtitle {{ font-size:0.87rem; color:{text_sub}; margin-bottom:1.5rem; line-height:1.5; }}
.page-divider {{
    height:3px;
    background:linear-gradient(90deg,{accent} 0%,{accent2} 50%,transparent 100%);
    border:none; border-radius:4px; margin-bottom:1.7rem;
}}

/* ── Stats grid ──────────────────────────────────────────── */
.stat-grid {{
    display:grid; grid-template-columns:repeat(4,1fr);
    gap:0.85rem; margin-bottom:1.4rem;
}}
@media(max-width:768px) {{ .stat-grid {{ grid-template-columns:repeat(2,1fr); }} }}
.stat-box {{
    background:{stat_bg}; border-radius:12px; padding:0.85rem 0.75rem;
    text-align:center; border:1px solid {border_col};
    box-shadow:{card_shadow}; transition:transform 0.25s, box-shadow 0.25s;
    position:relative; overflow:hidden;
}}
.stat-box::before {{
    content:''; position:absolute; top:0; left:0; right:0; height:3px;
    background:linear-gradient(90deg,{accent},{accent2});
}}
.stat-box:hover {{ transform:translateY(-3px); box-shadow:{card_hover}; }}
.stat-val {{ font-size:1.65rem; font-weight:900; color:{accent}; line-height:1; }}
.stat-lbl {{
    font-size:0.65rem; font-weight:700; color:{text_muted};
    text-transform:uppercase; letter-spacing:1.2px; margin-top:0.35rem;
}}

/* ── Section headers ─────────────────────────────────────── */
.sec-head {{ display:flex; align-items:center; gap:0.5rem; margin:1.2rem 0 0.2rem; }}
.sec-head h2 {{ font-size:1.1rem; font-weight:800; color:{sec_color}; margin:0; }}
.sec-line {{
    height:2px; background:linear-gradient(90deg,{accent} 0%,{accent2} 40%,transparent 100%);
    border:none; border-radius:4px; margin:0 0 0.8rem;
}}

/* ── Info / Warning boxes ────────────────────────────────── */
.info-box {{
    background:{info_bg}; border:1px solid {info_bdr};
    border-left:4px solid {accent};
    border-radius:12px; padding:1rem 1.4rem;
    font-size:0.86rem; color:{info_txt}; line-height:1.65; margin-bottom:1.2rem;
}}
.warn-box {{
    background:{warn_bg}; border:1px solid {warn_bdr};
    border-left:4px solid #f59e0b;
    border-radius:12px; padding:1rem 1.4rem;
    font-size:0.84rem; color:{warn_txt}; line-height:1.65; margin:0.9rem 0;
}}

/* ═══════════════════════════════════════════════════════════
   RESULT CARDS
   ═══════════════════════════════════════════════════════ */
.result-asd {{
    background:linear-gradient(135deg,#fef2f2 0%,#fee2e2 100%);
    border:2px solid #f87171; border-radius:20px; padding:2.2rem;
    text-align:center;
    box-shadow:0 12px 40px rgba(239,68,68,0.18);
}}
.result-nonasd {{
    background:linear-gradient(135deg,#ecfdf5 0%,#d1fae5 100%);
    border:2px solid #34d399; border-radius:20px; padding:2.2rem;
    text-align:center;
    box-shadow:0 12px 40px rgba(52,211,153,0.18);
}}
.result-icon {{ font-size:2.8rem; line-height:1; margin-bottom:0.6rem; }}
.result-label {{ font-size:2.1rem; font-weight:900; line-height:1; margin-bottom:0.35rem; }}
.result-label-asd {{ color:#dc2626; }}
.result-label-nonasd {{ color:#059669; }}
.result-sub {{ font-size:0.87rem; font-weight:500; }}
.result-sub-asd {{ color:#991b1b; }}
.result-sub-nonasd {{ color:#065f46; }}

/* ═══════════════════════════════════════════════════════════
   CONFIDENCE BOX
   ═══════════════════════════════════════════════════════ */
.conf-box {{
    background:{bg_card}; border-radius:20px; padding:2rem;
    border:1px solid {border_col}; box-shadow:{card_shadow};
}}
.conf-pct {{ font-size:3.2rem; font-weight:900; line-height:1; margin-bottom:0.25rem; }}
.conf-pct-asd {{ color:#dc2626; }}
.conf-pct-nonasd {{ color:#059669; }}
.bar-track {{
    background:{bg_card2}; border-radius:12px;
    height:20px; overflow:hidden; margin:0.9rem 0 0.45rem;
    box-shadow:inset 0 1px 4px rgba(0,0,0,0.08);
}}
.bar-fill {{ height:100%; border-radius:12px; transition:width 0.5s ease; }}
.bar-asd {{ background:linear-gradient(90deg,#fca5a5,#f87171,#ef4444,#dc2626); }}
.bar-nonasd {{ background:linear-gradient(90deg,#6ee7b7,#34d399,#10b981,#059669); }}
.bar-labels {{ display:flex; justify-content:space-between; font-size:0.67rem; color:{text_muted}; }}
.prob-row {{ display:grid; grid-template-columns:1fr 1fr; gap:0.8rem; margin-top:1.1rem; }}
.prob-cell {{
    background:{bg_card2}; border-radius:12px; padding:1rem;
    text-align:center; border:1px solid {border_col};
    transition:transform 0.2s;
}}
.prob-cell:hover {{ transform:translateY(-1px); }}
.prob-val {{ font-size:1.45rem; font-weight:900; }}
.prob-lbl {{
    font-size:0.64rem; font-weight:700; color:{text_muted};
    text-transform:uppercase; letter-spacing:0.7px; margin-top:0.12rem;
}}

/* ═══════════════════════════════════════════════════════════
   INTERPRETATION / CLINICAL CARDS
   ═══════════════════════════════════════════════════════ */
.interp-card {{
    background:{bg_card}; border-radius:16px; padding:1.6rem 1.9rem;
    border:1px solid {border_col}; box-shadow:{card_shadow}; margin-bottom:1rem;
}}
.interp-head {{
    font-size:0.93rem; font-weight:700; color:{accent};
    margin-bottom:0.55rem; display:flex; align-items:center; gap:0.4rem;
}}
.interp-body {{ font-size:0.87rem; color:{text_sub}; line-height:1.75; }}

/* ═══════════════════════════════════════════════════════════
   PATIENT SUMMARY
   ═══════════════════════════════════════════════════════ */
.pat-summary {{
    background:{bg_card}; border-radius:14px; padding:1.2rem 1.6rem;
    border:1px solid {border_col}; box-shadow:{card_shadow};
}}
.pat-row {{
    display:flex; justify-content:space-between; align-items:center;
    padding:0.5rem 0; border-bottom:1px solid {pat_bdr}; font-size:0.85rem;
}}
.pat-row:last-child {{ border-bottom:none; }}
.pat-key {{ color:{text_sub}; font-weight:500; }}
.pat-val {{ color:{text_main}; font-weight:700; }}

/* ═══════════════════════════════════════════════════════════
   FEATURE IMPORTANCE
   ═══════════════════════════════════════════════════════ */
.feat-row {{ display:flex; align-items:center; gap:0.8rem; margin-bottom:0.5rem; }}
.feat-name {{
    width:180px; text-align:right; color:{text_sub};
    font-weight:500; flex-shrink:0; font-size:0.76rem;
    white-space:nowrap; overflow:hidden; text-overflow:ellipsis;
}}
.feat-track {{
    flex:1; background:{bg_card2}; border-radius:6px;
    height:12px; overflow:hidden; box-shadow:inset 0 1px 3px rgba(0,0,0,0.06);
}}
.feat-fill {{
    height:100%; border-radius:6px;
    background:{feat_fill}; transition:width 0.4s ease;
}}
.feat-coef {{ width:45px; color:{accent}; font-weight:700; font-size:0.72rem; flex-shrink:0; }}
.feat-dir {{ font-size:0.67rem; color:{text_muted}; width:80px; flex-shrink:0; }}

/* ═══════════════════════════════════════════════════════════
   FORM GROUP CARDS
   ═══════════════════════════════════════════════════════ */
.fg-card {{
    background:{bg_card}; border-radius:16px;
    padding:1.4rem 1.8rem 0.5rem 1.8rem;
    border:1px solid {border_col}; box-shadow:{card_shadow};
    margin-bottom:1rem;
    border-left:4px solid {accent};
}}
.fg-title {{ font-size:0.95rem; font-weight:700; color:{accent}; margin-bottom:0.1rem; }}
.fg-desc  {{ font-size:0.77rem; color:{text_muted}; margin-bottom:0.85rem; line-height:1.5; }}

/* ═══════════════════════════════════════════════════════════
   HISTORY ROWS & BADGES
   ═══════════════════════════════════════════════════════ */
.hist-row {{
    background:{histrow_bg}; border-radius:14px; padding:1rem 1.4rem;
    margin-bottom:0.6rem; border:1px solid {border_col};
    box-shadow:{card_shadow}; transition:transform 0.2s, box-shadow 0.2s;
}}
.hist-row:hover {{ transform:translateY(-1px); box-shadow:{card_hover}; }}
.hist-badge-asd {{
    background:{badge_asd_bg}; color:{badge_asd_fg};
    padding:0.25rem 0.75rem; border-radius:50px;
    font-size:0.73rem; font-weight:700; letter-spacing:0.3px;
}}
.hist-badge-non {{
    background:{badge_non_bg}; color:{badge_non_fg};
    padding:0.25rem 0.75rem; border-radius:50px;
    font-size:0.73rem; font-weight:700; letter-spacing:0.3px;
}}

/* ═══════════════════════════════════════════════════════════
   AUTH PAGE
   ═══════════════════════════════════════════════════════ */
.auth-wrap {{
    max-width:400px; margin:0 auto;
    background:{auth_bg}; border-radius:18px;
    padding:1.4rem 1.8rem 1.4rem; box-shadow:{auth_shadow};
    border:1px solid {border_col};
    position:relative; overflow:hidden;
}}
.auth-wrap::before {{
    content:''; position:absolute; top:-60px; right:-60px;
    width:160px; height:160px;
    background:radial-gradient(circle,rgba(37,99,235,0.06) 0%,transparent 70%);
    border-radius:50%; pointer-events:none;
}}
.auth-logo {{ text-align:center; margin-bottom:0.9rem; }}
.auth-logo-icon {{ font-size:1.5rem; line-height:1; }}
.auth-logo h2 {{
    font-size:1.05rem; font-weight:900; color:{title_color};
    margin:0.25rem 0 0.1rem; letter-spacing:-0.3px;
}}
.auth-logo p {{ font-size:0.7rem; color:{text_sub}; margin:0; line-height:1.4; }}

/* ═══════════════════════════════════════════════════════════
   PROFILE
   ═══════════════════════════════════════════════════════ */
.profile-header {{
    display:flex; align-items:center; gap:1.5rem;
    background:{bg_card}; border-radius:20px; padding:1.8rem 2rem;
    box-shadow:{card_shadow}; margin-bottom:1.3rem; border:1px solid {border_col};
    position:relative; overflow:hidden;
}}
.profile-header::before {{
    content:''; position:absolute; top:0; left:0; right:0; height:3px;
    background:linear-gradient(90deg,{accent},{accent2});
}}
.avatar {{
    width:80px; height:80px; border-radius:50%; display:flex;
    align-items:center; justify-content:center; font-size:1.85rem;
    font-weight:900; color:white; flex-shrink:0;
    box-shadow:0 6px 24px rgba(0,0,0,0.2);
    position:relative;
}}
.avatar::after {{
    content:''; position:absolute; inset:-3px;
    border-radius:50%; border:2px solid {accent};
    opacity:0.4;
}}
.profile-name {{ font-size:1.38rem; font-weight:900; color:{title_color}; margin:0 0 0.22rem; }}
.profile-role {{ font-size:0.81rem; color:{text_sub}; font-weight:500; }}
.profile-meta {{ font-size:0.78rem; color:{text_muted}; margin-top:0.4rem; line-height:1.6; }}

/* ═══════════════════════════════════════════════════════════
   QUICK ACTION CARDS
   ═══════════════════════════════════════════════════════ */
.qa-card {{
    background:{bg_card}; border-radius:14px; padding:1.1rem;
    text-align:center; border:1px solid {border_col}; box-shadow:{card_shadow};
    transition:transform 0.28s, box-shadow 0.28s; min-height:120px;
    position:relative; overflow:hidden;
}}
.qa-card:hover {{ transform:translateY(-3px); box-shadow:{card_hover}; }}
.qa-icon {{ font-size:1.8rem; margin-bottom:0.35rem; }}
.qa-title {{ font-size:0.9rem; font-weight:800; color:{title_color}; margin-bottom:0.25rem; }}
.qa-desc  {{ font-size:0.75rem; color:{text_sub}; line-height:1.5; }}

/* ═══════════════════════════════════════════════════════════
   FOOTER
   ═══════════════════════════════════════════════════════ */
.app-footer {{
    text-align:center; padding:1rem 1rem 0.8rem;
    color:{text_muted}; font-size:0.72rem;
    border-top:1px solid {hr_col}; margin-top:1.5rem; line-height:1.8;
}}
.app-footer strong {{ color:{text_sub}; }}

/* ═══════════════════════════════════════════════════════════
   SCROLLBAR
   ═══════════════════════════════════════════════════════ */
::-webkit-scrollbar {{ width:6px; height:6px; }}
::-webkit-scrollbar-track {{ background:transparent; }}
::-webkit-scrollbar-thumb {{
    background:{input_bdr}; border-radius:6px;
}}
::-webkit-scrollbar-thumb:hover {{ background:{accent}; }}

/* ═══════════════════════════════════════════════════════════
   DATAFRAME TABLES
   ═══════════════════════════════════════════════════════ */
.stDataFrame {{
    border-radius:12px !important; overflow:hidden !important;
    border:1px solid {border_col} !important;
}}
</style>
"""
