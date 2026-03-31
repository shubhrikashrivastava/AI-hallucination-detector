import streamlit as st
import pandas as pd
import plotly.express as px
import re
from styles import apply_sentinel_design
from detector_logic import run_sentinel_audit
from database import init_db, get_cached_audit, save_audit_to_db, get_all_history

init_db()
st.set_page_config(page_title="VERIFY.AI Sentinel", layout="wide")
apply_sentinel_design()

# Session State Initialization
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'report' not in st.session_state: st.session_state.report = ""
if 'score' not in st.session_state: st.session_state.score = 0

# --- AUTH GATE ---
if not st.session_state.logged_in:
    _, col, _ = st.columns([1, 1.2, 1])
    with col:
        st.markdown("<h1 style='text-align:center; color:#00f2fe;'>VERIFY.AI</h1>", unsafe_allow_html=True)
        u = st.text_input("IDENTIFIER")
        p = st.text_input("KEY", type="password")
        if st.button("INITIALIZE"):
            if u == "admin" and p == "noida2026":
                st.session_state.logged_in = True
                st.rerun()
    st.stop()

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("<h2 style='color:#00f2fe;'>SENTINEL SUITE</h2>", unsafe_allow_html=True)
    nav = st.radio("NAVIGATE", ["🏠 Dashboard", "🤖 Agents", "📊 Reports", "⚙️ Settings"])
    st.markdown("---")
    st.markdown("### 🕒 Recent History")
    for h_text, h_score, h_time in get_all_history()[:5]:
        st.caption(f"Score: {h_score}% | {h_time[11:16]}")
        st.markdown(f"<div style='font-size:10px; color:#888;'>{h_text[:40]}...</div>", unsafe_allow_html=True)

# --- DASHBOARD ---
if nav == "🏠 Dashboard":
    c1, c2 = st.columns([1.6, 1])
    with c1:
        st.markdown("### 🧬 Analysis Engine")
        content = st.text_area("Content", placeholder="Paste text to verify...", height=300, label_visibility="collapsed")
        if st.button("🚀 INITIATE AUDIT"):
            if content:
                cached = get_cached_audit(content)
                if cached:
                    st.session_state.report, st.session_state.score = cached
                    st.toast("Retrieved from Sentinel Cache 🛡️")
                else:
                    with st.status("Swarm active: Analyzing...", expanded=True):
                        res = run_sentinel_audit(content)
                        st.session_state.report = str(res)
                        scores = re.findall(r"(\d+)/100", st.session_state.report)
                        st.session_state.score = int(scores[0]) if scores else 50
                        save_audit_to_db(content, st.session_state.report, st.session_state.score)
                st.rerun()

    with c2:
        st.markdown(f"<div class='glass-panel active-glow' style='text-align:center;'><p style='font-size:10px;'>TRUST INDEX</p><h1 class='trust-val'>{st.session_state.score}%</h1></div>", unsafe_allow_html=True)
        if st.session_state.report:
            t1, t2 = st.tabs(["📝 Audit Report", "✨ Factual Rewrite"])
            t1.markdown(f"<div class='glass-panel' style='font-size:13px;'>{st.session_state.report}</div>", unsafe_allow_html=True)
            # Refiner's final answer is at the bottom of the report
            t2.success(f"**Verified Content:**\n\n{st.session_state.report.split('###')[-1]}")

# --- OTHER TABS ---
elif nav == "📊 Reports":
    st.title("📊 Hallucination Analytics")
    st.markdown("<div class='glass-panel'>Common Hallucination Types (Q1 2026)</div>", unsafe_allow_html=True)
    df = pd.DataFrame({'Type': ['Fact', 'Logic', 'Source', 'Tone'], 'Freq': [38, 24, 22, 16]})
    st.plotly_chart(px.bar(df, x='Type', y='Freq', template="plotly_dark", color_discrete_sequence=['#00f2fe']))

elif nav == "🤖 Agents":
    st.title("🤖 Agent Swarm Trace")
    st.code(st.session_state.report if st.session_state.report else "No active audit found.", language="markdown")

elif nav == "⚙️ Settings":
    st.title("⚙️ System Config")
    st.markdown("<div class='glass-panel'>API Status: <span style='color:green;'>Active</span></div>", unsafe_allow_html=True)
