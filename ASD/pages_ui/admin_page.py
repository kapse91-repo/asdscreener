"""
Admin Panel — System-wide user management, analytics, and audit log.
Only accessible to users with is_admin=1 or username='admin'.
"""
import json, csv, io
import streamlit as st
from datetime import datetime

from helpers.auth import (
    get_all_users, get_all_predictions, get_system_stats,
    admin_delete_user, admin_toggle_admin, is_admin
)
from helpers.styles import get_css
from helpers.profile_page_helpers import get_initials


# ── Helpers ────────────────────────────────────────────────────────────
SEX_MAP = {"1": "Male", "2": "Female"}


def _predictions_csv(records: list[dict]) -> str:
    buf = io.StringIO()
    fields = ["id", "created_at", "username", "full_name",
              "prediction", "asd_probability", "confidence",
              "patient_age", "patient_sex"]
    w = csv.DictWriter(buf, fieldnames=fields, extrasaction="ignore")
    w.writeheader()
    for r in records:
        row = {k: r.get(k, "") for k in fields}
        row["asd_probability"] = f"{r.get('asd_probability',0)*100:.1f}%"
        row["confidence"]      = f"{r.get('confidence',0)*100:.1f}%"
        row["patient_sex"]     = SEX_MAP.get(str(r.get("patient_sex","")), str(r.get("patient_sex","")))
        w.writerow(row)
    return buf.getvalue()


def _users_csv(users: list[dict]) -> str:
    buf = io.StringIO()
    fields = ["id", "username", "email", "full_name", "role",
              "institution", "is_admin", "created_at", "last_login"]
    w = csv.DictWriter(buf, fieldnames=fields, extrasaction="ignore")
    w.writeheader()
    for u in users:
        w.writerow({k: u.get(k, "") for k in fields})
    return buf.getvalue()


# ── Main ────────────────────────────────────────────────────────────────
def show(user: dict):
    st.markdown(get_css(), unsafe_allow_html=True)

    # Guard: non-admins bounce back
    if not is_admin(user):
        st.error("⛔ Access denied — Admin privileges required.")
        if st.button("← Back to Dashboard"):
            st.session_state.page = "dashboard"; st.rerun()
        return

    if st.button("← Back to Dashboard", key="admin_back"):
        st.session_state.page = "dashboard"; st.rerun()

    st.markdown("""
<div class="page-title">🛡️ Admin Panel</div>
<div class="page-subtitle">System-wide management console — user accounts, assessments, analytics, and audit log.</div>
<hr class="page-divider">""", unsafe_allow_html=True)

    # ── System stats bar ──────────────────────────────────────────────
    s = get_system_stats()
    st.markdown(f"""
<div class="stat-grid" style="grid-template-columns:repeat(7,1fr);">
  <div class="stat-box">
    <div class="stat-val">{s['total_users']}</div>
    <div class="stat-lbl">Total Users</div>
  </div>
  <div class="stat-box">
    <div class="stat-val">{s['total_preds']}</div>
    <div class="stat-lbl">Total Assessments</div>
  </div>
  <div class="stat-box">
    <div class="stat-val" style="color:#dc2626;">{s['asd_preds']}</div>
    <div class="stat-lbl">ASD Detected</div>
  </div>
  <div class="stat-box">
    <div class="stat-val" style="color:#059669;">{s['nonasd_preds']}</div>
    <div class="stat-lbl">Non-ASD</div>
  </div>
  <div class="stat-box">
    <div class="stat-val">{s['avg_confidence']}%</div>
    <div class="stat-lbl">Avg. Confidence</div>
  </div>
  <div class="stat-box">
    <div class="stat-val" style="color:#7c3aed;">{s['today_preds']}</div>
    <div class="stat-lbl">Today's Assessments</div>
  </div>
  <div class="stat-box">
    <div class="stat-val" style="color:#0891b2;">{s['today_logins']}</div>
    <div class="stat-lbl">Today's Logins</div>
  </div>
</div>""", unsafe_allow_html=True)

    # ── Tabs ──────────────────────────────────────────────────────────
    t1, t2, t3, t4 = st.tabs([
        "👥  Users",
        "📋  All Assessments",
        "📈  Analytics",
        "🕒  Login Audit",
    ])

    # ══════════════════════════════════════════════════════════════════
    # TAB 1 — USER MANAGEMENT
    # ══════════════════════════════════════════════════════════════════
    with t1:
        users = get_all_users()
        st.markdown(f"""
<div class="sec-head"><h2>👥 Registered Users ({len(users)})</h2></div>
<hr class="sec-line">""", unsafe_allow_html=True)

        # Search + export row
        sc1, sc2, sc3 = st.columns([2, 1, 1])
        with sc1:
            search = st.text_input("🔍 Search users", placeholder="Name, username, email, institution…",
                                   label_visibility="collapsed")
        with sc2:
            role_f = st.selectbox("Filter by Role",
                                  ["All", "Admin", "Clinician", "Researcher", "Student",
                                   "Parent / Caregiver", "Other"],
                                  label_visibility="collapsed")
        with sc3:
            st.download_button("📥 Export Users CSV", data=_users_csv(users),
                               file_name="asd_users.csv", mime="text/csv",
                               use_container_width=True)

        # Filter
        filtered_u = users
        if search:
            q = search.lower()
            filtered_u = [u for u in filtered_u if
                          q in (u.get("username") or "").lower() or
                          q in (u.get("full_name") or "").lower() or
                          q in (u.get("email") or "").lower() or
                          q in (u.get("institution") or "").lower()]
        if role_f != "All":
            filtered_u = [u for u in filtered_u if
                          (u.get("role") or "").lower() == role_f.lower()]

        st.markdown(
            f'<div style="font-size:0.8rem;color:#64748b;margin-bottom:0.8rem;">'
            f'Showing <strong>{len(filtered_u)}</strong> of <strong>{len(users)}</strong> users</div>',
            unsafe_allow_html=True
        )

        # User cards
        for u in filtered_u:
            uid      = u["id"]
            uname    = u.get("username", "—")
            fname    = u.get("full_name") or uname
            email    = u.get("email", "—")
            role     = (u.get("role") or "").capitalize()
            inst     = u.get("institution") or "—"
            joined   = (u.get("created_at") or "—")[:10]
            last     = (u.get("last_login") or "Never")[:16]
            av_col   = u.get("avatar_color") or "#1e3a8a"
            inits    = get_initials(fname)
            admin_fl = bool(u.get("is_admin"))
            admin_badge = '<span style="background:#fef9c3;color:#854d0e;padding:0.18rem 0.55rem;border-radius:50px;font-size:0.68rem;font-weight:700;margin-left:0.5rem;">ADMIN</span>' if admin_fl else ""

            with st.expander(f"{'🛡️' if admin_fl else '👤'}  {fname}  (@{uname})  ·  {role}  ·  Last login: {last}"):
                col_av, col_det, col_act = st.columns([1, 4, 2])

                with col_av:
                    st.markdown(f"""
<div style="text-align:center;padding-top:0.5rem;">
  <div class="avatar" style="background:{av_col};margin:0 auto;width:60px;height:60px;font-size:1.4rem;">{inits}</div>
  <div style="font-size:0.7rem;color:#94a3b8;margin-top:0.5rem;">ID #{uid}</div>
</div>""", unsafe_allow_html=True)

                with col_det:
                    st.markdown(f"""
<div class="pat-summary">
  <div class="pat-row"><span class="pat-key">Full Name</span><span class="pat-val">{fname} {admin_badge}</span></div>
  <div class="pat-row"><span class="pat-key">Username</span><span class="pat-val">@{uname}</span></div>
  <div class="pat-row"><span class="pat-key">Email</span><span class="pat-val">{email}</span></div>
  <div class="pat-row"><span class="pat-key">Role</span><span class="pat-val">{role}</span></div>
  <div class="pat-row"><span class="pat-key">Institution</span><span class="pat-val">{inst}</span></div>
  <div class="pat-row"><span class="pat-key">Registered</span><span class="pat-val">{joined}</span></div>
  <div class="pat-row"><span class="pat-key">Last Login</span><span class="pat-val">{last}</span></div>
</div>""", unsafe_allow_html=True)

                with col_act:
                    st.markdown("<div style='padding-top:0.4rem;'></div>", unsafe_allow_html=True)

                    # Toggle admin
                    tog_label = "🔓 Revoke Admin" if admin_fl else "🛡️ Grant Admin"
                    if uname != "admin":
                        if st.button(tog_label, key=f"tog_{uid}", use_container_width=True):
                            ok, msg = admin_toggle_admin(uid)
                            if ok:
                                st.success(msg)
                            else:
                                st.error(msg)
                            st.rerun()

                    # Delete
                    if uname != "admin" and uid != user["id"]:
                        confirm_key = f"del_confirm_{uid}"
                        if st.session_state.get(confirm_key):
                            st.warning("⚠️ Confirm deletion?")
                            c1d, c2d = st.columns(2)
                            with c1d:
                                if st.button("✅ Yes, Delete", key=f"del_yes_{uid}",
                                             use_container_width=True):
                                    ok, msg = admin_delete_user(uid)
                                    st.session_state.pop(confirm_key, None)
                                    if ok:
                                        st.success(msg)
                                    else:
                                        st.error(msg)
                                    st.rerun()
                            with c2d:
                                if st.button("❌ Cancel", key=f"del_no_{uid}",
                                             use_container_width=True):
                                    st.session_state.pop(confirm_key, None)
                                    st.rerun()
                        else:
                            if st.button("🗑️ Delete User", key=f"del_{uid}",
                                         use_container_width=True):
                                st.session_state[confirm_key] = True
                                st.rerun()

    # ══════════════════════════════════════════════════════════════════
    # TAB 2 — ALL ASSESSMENTS
    # ══════════════════════════════════════════════════════════════════
    with t2:
        all_preds = get_all_predictions(limit=200)
        st.markdown(f"""
<div class="sec-head"><h2>📋 All Assessments ({len(all_preds)})</h2></div>
<hr class="sec-line">""", unsafe_allow_html=True)

        # Filters
        af1, af2, af3, af4 = st.columns([2, 1, 1, 1])
        with af1:
            search_p = st.text_input("🔍 Search by user", placeholder="Username or name…",
                                     label_visibility="collapsed", key="pred_search")
        with af2:
            pred_f = st.selectbox("Prediction", ["All", "ASD", "Non-ASD"],
                                  label_visibility="collapsed", key="pred_pf")
        with af3:
            sex_f = st.selectbox("Sex", ["All", "Male", "Female"],
                                 label_visibility="collapsed", key="pred_sf")
        with af4:
            st.download_button("📥 Export CSV", data=_predictions_csv(all_preds),
                               file_name="asd_all_assessments.csv", mime="text/csv",
                               use_container_width=True, key="pred_dl")

        fp2 = list(all_preds)
        if search_p:
            q = search_p.lower()
            fp2 = [r for r in fp2 if q in (r.get("username") or "").lower()
                   or q in (r.get("full_name") or "").lower()]
        if pred_f != "All":
            fp2 = [r for r in fp2 if r["prediction"] == pred_f]
        if sex_f == "Male":
            fp2 = [r for r in fp2 if str(r.get("patient_sex","")) == "1"]
        elif sex_f == "Female":
            fp2 = [r for r in fp2 if str(r.get("patient_sex","")) == "2"]

        st.markdown(
            f'<div style="font-size:0.8rem;color:#64748b;margin-bottom:0.8rem;">'
            f'Showing <strong>{len(fp2)}</strong> records</div>',
            unsafe_allow_html=True
        )

        # Table-style list
        for i, rec in enumerate(fp2):
            is_asd = rec["prediction"] == "ASD"
            badge  = "hist-badge-asd" if is_asd else "hist-badge-non"
            conf   = rec.get("confidence", 0) * 100
            asdp   = rec.get("asd_probability", 0) * 100
            sex_d  = SEX_MAP.get(str(rec.get("patient_sex","")), "—")
            uname  = rec.get("username", "—")
            fname  = rec.get("full_name") or uname
            ts     = (rec.get("created_at") or "—")[:16]
            age    = rec.get("patient_age", "—")

            with st.expander(
                f"#{i+1}  ·  {ts}  ·  {rec['prediction']}  ·  "
                f"@{uname}  ·  Age {age}  ·  {conf:.1f}% conf"
            ):
                dc, di = st.columns([1, 2])
                with dc:
                    bc = "#dc2626" if is_asd else "#059669"
                    st.markdown(f"""
<div class="pat-summary">
  <div class="pat-row"><span class="pat-key">Result</span>
    <span class="pat-val" style="color:{bc};">{rec['prediction']}</span></div>
  <div class="pat-row"><span class="pat-key">Clinician</span>
    <span class="pat-val">{fname} (@{uname})</span></div>
  <div class="pat-row"><span class="pat-key">Date</span>
    <span class="pat-val">{ts}</span></div>
  <div class="pat-row"><span class="pat-key">Age</span>
    <span class="pat-val">{age}</span></div>
  <div class="pat-row"><span class="pat-key">Sex</span>
    <span class="pat-val">{sex_d}</span></div>
  <div class="pat-row"><span class="pat-key">ASD Probability</span>
    <span class="pat-val">{asdp:.1f}%</span></div>
  <div class="pat-row"><span class="pat-key">Confidence</span>
    <span class="pat-val">{conf:.1f}%</span></div>
</div>""", unsafe_allow_html=True)
                with di:
                    try:
                        inp = json.loads(rec.get("inputs_json", "{}"))
                        if inp:
                            from helpers.feature_config import FEATURE_GROUPS as FG
                            lmap = {fn: fc["label"] for gf in FG.values() for fn, fc in gf.items()}
                            srev = {fn: {v: k for k, v in fc["options"].items()}
                                    for gf in FG.values() for fn, fc in gf.items()
                                    if fc["type"] == "select"}
                            rows_html = "".join(
                                f'<div class="pat-row">'
                                f'<span class="pat-key">{lmap.get(k,k)}</span>'
                                f'<span class="pat-val">{srev.get(k,{}).get(v,v)}</span>'
                                f'</div>'
                                for k, v in inp.items()
                            )
                            st.markdown(
                                f'<div class="pat-summary" style="max-height:240px;overflow-y:auto;">'
                                f'{rows_html}</div>',
                                unsafe_allow_html=True
                            )
                    except Exception:
                        st.caption("Input detail unavailable.")

    # ══════════════════════════════════════════════════════════════════
    # TAB 3 — ANALYTICS
    # ══════════════════════════════════════════════════════════════════
    with t3:
        st.markdown('<div class="sec-head"><h2>📈 Platform Analytics</h2></div><hr class="sec-line">',
                    unsafe_allow_html=True)

        # Prediction distribution donut (via st.bar_chart polyfill with HTML)
        total_p = s["total_preds"]
        if total_p > 0:
            asd_pct  = s["asd_preds"]  / total_p * 100
            nasd_pct = s["nonasd_preds"] / total_p * 100

            a1, a2 = st.columns(2)
            with a1:
                st.markdown(f"""
<div class="card" style="text-align:center;">
  <div class="interp-head">🔵 Prediction Distribution</div>
  <div style="margin:1rem 0;">
    <div style="display:flex;align-items:center;gap:0.7rem;margin-bottom:0.6rem;">
      <div style="flex:1;background:#fee2e2;border-radius:8px;height:28px;overflow:hidden;">
        <div style="background:#dc2626;height:100%;width:{asd_pct:.1f}%;border-radius:8px;
             display:flex;align-items:center;justify-content:flex-end;padding-right:0.4rem;">
          <span style="color:white;font-size:0.72rem;font-weight:700;">{asd_pct:.1f}%</span>
        </div>
      </div>
      <span style="font-size:0.8rem;font-weight:700;color:#dc2626;width:40px;">ASD</span>
    </div>
    <div style="display:flex;align-items:center;gap:0.7rem;">
      <div style="flex:1;background:#dcfce7;border-radius:8px;height:28px;overflow:hidden;">
        <div style="background:#059669;height:100%;width:{nasd_pct:.1f}%;border-radius:8px;
             display:flex;align-items:center;justify-content:flex-end;padding-right:0.4rem;">
          <span style="color:white;font-size:0.72rem;font-weight:700;">{nasd_pct:.1f}%</span>
        </div>
      </div>
      <span style="font-size:0.8rem;font-weight:700;color:#059669;width:40px;">Non</span>
    </div>
  </div>
  <div style="font-size:0.75rem;color:#94a3b8;">Based on {total_p} total assessments</div>
</div>""", unsafe_allow_html=True)

            with a2:
                st.markdown(f"""
<div class="card">
  <div class="interp-head">📊 Key Metrics</div>
  <div class="pat-summary" style="margin-top:0.6rem;">
    <div class="pat-row"><span class="pat-key">Total Users</span>
      <span class="pat-val">{s['total_users']}</span></div>
    <div class="pat-row"><span class="pat-key">Total Assessments</span>
      <span class="pat-val">{s['total_preds']}</span></div>
    <div class="pat-row"><span class="pat-key">ASD Rate</span>
      <span class="pat-val" style="color:#dc2626;">{asd_pct:.1f}%</span></div>
    <div class="pat-row"><span class="pat-key">Non-ASD Rate</span>
      <span class="pat-val" style="color:#059669;">{nasd_pct:.1f}%</span></div>
    <div class="pat-row"><span class="pat-key">Avg. Confidence</span>
      <span class="pat-val">{s['avg_confidence']}%</span></div>
    <div class="pat-row"><span class="pat-key">Today's Assessments</span>
      <span class="pat-val" style="color:#7c3aed;">{s['today_preds']}</span></div>
    <div class="pat-row"><span class="pat-key">Today's Logins</span>
      <span class="pat-val" style="color:#0891b2;">{s['today_logins']}</span></div>
  </div>
</div>""", unsafe_allow_html=True)

        # Top users leaderboard
        st.markdown('<div class="sec-head"><h2>🏆 Most Active Users</h2></div><hr class="sec-line">',
                    unsafe_allow_html=True)
        if s["user_counts"]:
            max_cnt = max((uc["cnt"] for uc in s["user_counts"]), default=1) or 1
            bars_html = "".join(
                f'<div style="display:flex;align-items:center;gap:0.7rem;margin-bottom:0.55rem;">'
                f'<div style="width:140px;font-size:0.8rem;font-weight:600;color:#475569;'
                f'    white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">'
                f'  {uc.get("full_name") or uc["username"]}</div>'
                f'<div style="flex:1;background:#f1f5f9;border-radius:8px;height:18px;overflow:hidden;">'
                f'  <div style="background:linear-gradient(90deg,#06b6d4,#2563eb);height:100%;'
                f'       width:{uc["cnt"]/max_cnt*100:.0f}%;border-radius:8px;"></div>'
                f'</div>'
                f'<div style="width:40px;font-size:0.82rem;font-weight:800;color:#2563eb;">'
                f'  {uc["cnt"]}</div>'
                f'</div>'
                for uc in s["user_counts"]
            )
            st.markdown(f'<div class="interp-card"><div class="interp-head">Assessments per User</div>'
                        f'<div style="margin-top:0.8rem;">{bars_html}</div></div>',
                        unsafe_allow_html=True)

        # Per-user detailed chart using st.bar_chart
        all_preds_an = get_all_predictions(limit=500)
        if all_preds_an:
            import pandas as pd
            df = pd.DataFrame(all_preds_an)
            df["date"] = pd.to_datetime(df["created_at"]).dt.date.astype(str)

            st.markdown('<div class="sec-head"><h2>📅 Assessments Over Time</h2></div><hr class="sec-line">',
                        unsafe_allow_html=True)
            date_counts = df.groupby("date").size().reset_index(name="Assessments")
            date_counts = date_counts.set_index("date")
            st.bar_chart(date_counts, height=220)

    # ══════════════════════════════════════════════════════════════════
    # TAB 4 — LOGIN AUDIT
    # ══════════════════════════════════════════════════════════════════
    with t4:
        st.markdown('<div class="sec-head"><h2>🕒 Recent Login Activity</h2></div><hr class="sec-line">',
                    unsafe_allow_html=True)

        all_users = get_all_users()
        logins = [u for u in all_users if u.get("last_login")]
        logins.sort(key=lambda x: x.get("last_login",""), reverse=True)

        if not logins:
            st.markdown('<div class="info-box">No login activity recorded yet.</div>',
                        unsafe_allow_html=True)
        else:
            # Stats
            today = datetime.now().strftime("%Y-%m-%d")
            today_l = [u for u in logins if (u.get("last_login","")).startswith(today)]
            never_l = [u for u in all_users if not u.get("last_login")]

            st.markdown(f"""
<div class="stat-grid" style="grid-template-columns:repeat(3,1fr);max-width:600px;">
  <div class="stat-box"><div class="stat-val">{len(logins)}</div><div class="stat-lbl">Ever Logged In</div></div>
  <div class="stat-box"><div class="stat-val" style="color:#0891b2;">{len(today_l)}</div><div class="stat-lbl">Today</div></div>
  <div class="stat-box"><div class="stat-val" style="color:#f59e0b;">{len(never_l)}</div><div class="stat-lbl">Never Logged In</div></div>
</div>""", unsafe_allow_html=True)

            st.write("")

            # Login rows
            for u in logins:
                fname   = u.get("full_name") or u.get("username","—")
                uname   = u.get("username","—")
                role    = (u.get("role") or "").capitalize()
                last    = u.get("last_login","—")[:16]
                av_col  = u.get("avatar_color") or "#1e3a8a"
                inits   = get_initials(fname)
                is_adm  = bool(u.get("is_admin"))
                is_today = (u.get("last_login","")).startswith(today)
                now_badge = '<span style="background:#dcfce7;color:#059669;font-size:0.67rem;font-weight:700;padding:0.15rem 0.5rem;border-radius:50px;margin-left:0.4rem;">TODAY</span>' if is_today else ""

                st.markdown(f"""
<div class="hist-row" style="display:flex;align-items:center;gap:0.9rem;">
  <div class="avatar" style="background:{av_col};width:38px;height:38px;font-size:0.85rem;flex-shrink:0;">{inits}</div>
  <div style="flex:1;">
    <div style="font-size:0.9rem;font-weight:700;color:#0f172a;">{fname} {now_badge}</div>
    <div style="font-size:0.76rem;color:#64748b;">@{uname} &nbsp;·&nbsp; {role}</div>
  </div>
  <div style="font-size:0.8rem;color:#94a3b8;text-align:right;">
    🕒 {last}
    {"&nbsp;&nbsp;🛡️" if is_adm else ""}
  </div>
</div>""", unsafe_allow_html=True)

            # Never-logged-in section
            if never_l:
                st.markdown('<div class="sec-head" style="margin-top:1.5rem;"><h2>⚠️ Never Logged In</h2></div><hr class="sec-line">',
                            unsafe_allow_html=True)
                for u in never_l:
                    fname  = u.get("full_name") or u.get("username","—")
                    uname  = u.get("username","—")
                    joined = (u.get("created_at","—"))[:10]
                    st.markdown(f"""
<div class="hist-row" style="display:flex;align-items:center;gap:0.9rem;opacity:0.7;">
  <div style="flex:1;">
    <div style="font-size:0.88rem;font-weight:700;color:#0f172a;">{fname} <span style="color:#94a3b8;font-size:0.76rem;">(@{uname})</span></div>
    <div style="font-size:0.74rem;color:#64748b;">Registered: {joined}</div>
  </div>
  <span style="font-size:0.75rem;background:#fef9c3;color:#854d0e;padding:0.2rem 0.55rem;border-radius:50px;font-weight:700;">INACTIVE</span>
</div>""", unsafe_allow_html=True)

    st.markdown("""
<div class="app-footer">
  <strong>ASD Prediction System</strong> — Admin Console<br>Built by Yogadi
</div>""", unsafe_allow_html=True)
