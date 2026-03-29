import streamlit as st
import plotly.graph_objects as go
from detector_logic import run_hallucination_check
import re
import time

# --- 1. PAGE CONFIG & THEME ---
st.set_page_config(page_title="VERIFY.AI | Agentic Audit", layout="wide", initial_sidebar_state="expanded")

# Advanced Cyberpunk Glassmorphism CSS
st.markdown("""
    <style>
    /* Animated Deep Sea Gradient */
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #020617 0%, #0f172a 50%, #020617 100%);
        background-size: 400% 400%;
        animation: gradientBG 15s ease infinite;
    }
    @keyframes gradientBG {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    /* Glass Cards */
    .stTextArea textarea {
        background: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(0, 242, 254, 0.2) !important;
        color: #e2e8f0 !important;
        border-radius: 15px;
    }
    
    .report-card {
        background: rgba(15, 23, 42, 0.6);
        backdrop-filter: blur(12px);
        border-radius: 20px;
        padding: 25px;
        border: 1px solid rgba(0, 242, 254, 0.3);
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
        margin-top: 20px;
    }

    /* Glow Button */
    .stButton > button {
        background: linear-gradient(90deg, #00f2fe 0%, #4facfe 100%);
        color: #020617 !important;
        font-weight: 800;
        letter-spacing: 1px;
        border: none;
        border-radius: 12px;
        padding: 0.6rem 2rem;
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        transform: scale(1.02);
        box-shadow: 0 0 20px rgba(0, 242, 254, 0.6);
    }
    </style>
""", unsafe_allow_html=True)

# --- 2. LOGIC HELPERS ---
def extract_score(text):
    """Robust regex to find score like 85/100 or Score: 85%"""
    match = re.search(r"(\d+)\s*/\s*100|Score:\s*(\d+)|(\d+)%", text)
    if match:
        return int(next(g for g in match.groups() if g is not None))
    return 70  # Default if parsing fails

def draw_gauge(score):
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = score,
        domain = {'x': [0, 1], 'y': [0, 1]},
        gauge = {
            'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "#00f2fe"},
            'bar': {'color': "#00f2fe"},
            'bgcolor': "rgba(0,0,0,0)",
            'steps': [
                {'range': [0, 50], 'color': 'rgba(239, 68, 68, 0.2)'},
                {'range': [50, 80], 'color': 'rgba(234, 179, 8, 0.2)'},
                {'range': [80, 100], 'color': 'rgba(34, 197, 94, 0.2)'}
            ],
            'threshold': {'line': {'color': "white", 'width': 4}, 'thickness': 0.75, 'value': score}
        }
    ))
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', font={'color': "#00f2fe", 'family': "monospace"}, height=300, margin=dict(l=20, r=20, t=50, b=20))
    return fig

# --- 3. UI LAYOUT ---
st.sidebar.title("🛠️ Settings")
st.sidebar.info("Model: Llama-3.3-70b (Heavy) & Llama-3.1-8b (Fast)")
if st.sidebar.button("Clear History"):
    st.session_state.clear()
    st.rerun()

st.markdown("<h1 style='text-align: center; color: #00f2fe; text-shadow: 0 0 10px #00f2fe;'>V E R I F Y . A I</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #94a3b8;'>Multi-Agent Hallucination Detection & Correction Swarm</p>", unsafe_allow_html=True)

col1, col2 = st.columns([1.6, 1], gap="medium")

with col1:
    st.markdown("### 📝 Input Content")
    input_text = st.text_area("Paste text to verify...", height=300, label_visibility="collapsed")
    
    if st.button("RUN AGENTIC AUDIT"):
        if not input_text:
            st.warning("Please enter some text first!")
        else:
            with st.status("🔍 Initializing Agent Swarm...", expanded=True) as status:
                st.write("🕵️‍♂️ Extracting Factual Claims...")
                # The logic call
                result = run_hallucination_check(input_text)
                
                st.write("🌍 Cross-Referencing with Live Web Data...")
                time.sleep(1) # Visual pacing
                
                st.write("⚖️ Auditing Contradictions...")
                final_output = str(result)
                
                status.update(label="✅ Audit Complete!", state="complete", expanded=False)
            
            # Store in session state
            st.session_state.report = final_output
            st.session_state.score = extract_score(final_output)
            st.balloons()

with col2:
    st.markdown("### 📊 Trust Index")
    score = st.session_state.get('score', 0)
    st.plotly_chart(draw_gauge(score), use_container_width=True)
    
    if score < 60 and score > 0:
        st.error(f"High Hallucination Risk Detected ({score}%)")
    elif score >= 80:
        st.success(f"Content Verified as Reliable ({score}%)")

# --- 4. FINAL REPORT DISPLAY ---
if 'report' in st.session_state:
    st.divider()
    st.markdown("### 🏆 Final Audited Result")
    st.markdown(f"""
    <div class="report-card">
        {st.session_state.report}
    </div>
    """, unsafe_allow_html=True)
