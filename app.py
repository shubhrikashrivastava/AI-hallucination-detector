import streamlit as st
import plotly.graph_objects as go
from detector_logic import run_hallucination_check
import re

# 1. Page Config
st.set_page_config(page_title="VERIFY.AI", layout="wide", initial_sidebar_state="collapsed")

# 2. State Management
if 'score' not in st.session_state: st.session_state.score = 0
if 'report' not in st.session_state: st.session_state.report = ""

# 3. CSS Styling
st.markdown("""
    <style>
    [data-testid="stAppViewContainer"] { background: radial-gradient(circle at top right, #0d1117, #010409); color: #e6edf3; }
    .report-card { background: rgba(255, 255, 255, 0.03); backdrop-filter: blur(15px); border-radius: 15px; padding: 25px; border: 1px solid rgba(255, 255, 255, 0.1); margin-bottom: 20px; }
    .stButton > button { background: linear-gradient(90deg, #00f2fe 0%, #4facfe 100%); color: black !important; font-weight: 700; border-radius: 10px; width: 100%; }
    #MainMenu, footer, header { visibility: hidden; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center; color: #00f2fe; letter-spacing: 5px;'>V E R I F Y . A I</h1>", unsafe_allow_html=True)

col1, col2 = st.columns([1.5, 1], gap="large")

def draw_gauge(score):
    fig = go.Figure(go.Indicator(
        mode = "gauge+number", value = score,
        title = {'text': "Trust Index %", 'font': {'color': "#00f2fe"}},
        gauge = { 'axis': {'range': [0, 100]}, 'bar': {'color': "#00f2fe"}, 'steps': [{'range': [0, 40], 'color': '#3e0e0e'}, {'range': [40, 75], 'color': '#3e3e0e'}, {'range': [75, 100], 'color': '#0e3e1e'}]}
    ))
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', font={'color': "white"}, height=350)
    return fig

with col1:
    st.markdown("### 📥 Source Content")
    input_text = st.text_area("", placeholder="Paste AI-generated text here...", height=250, label_visibility="collapsed")
    if st.button("EXECUTE AGENTIC AUDIT"):
        if input_text:
            with st.status("🚀 Orchestrating Agent Swarm...", expanded=True) as status:
                result = run_hallucination_check(input_text)
                status.update(label="✅ Audit Complete", state="complete", expanded=False)
            
            # Parse Score
            final_text = str(result)
            scores = re.findall(r"(\d+)/100|Score: (\d+)|(\d+)%", final_text)
            flat_scores = [s for sub in scores for s in sub if s]
            st.session_state.score = int(flat_scores[0]) if flat_scores else 85
            st.session_state.report = final_text
            st.rerun()
        else:
            st.error("Please provide text content.")

with col2:
    st.markdown("### 📊 Analytics")
    st.plotly_chart(draw_gauge(st.session_state.score), use_container_width=True, key="dynamic_gauge")

if st.session_state.report:
    st.markdown("### 🏆 Verified Output")
    st.markdown(f'<div class="report-card" style="border-left: 5px solid #00f2fe;">{st.session_state.report}</div>', unsafe_allow_html=True)
    st.balloons()