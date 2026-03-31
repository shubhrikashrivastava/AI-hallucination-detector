import streamlit as st

def apply_sentinel_design():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;800&family=Space+Grotesk:wght@400;500&display=swap');
    
    [data-testid="stAppViewContainer"] { background-color: #10141a !important; color: #dfe2eb; font-family: 'Inter', sans-serif; }
    [data-testid="stSidebar"] { background-color: #181c22 !important; border-right: 1px solid rgba(255, 255, 255, 0.05); }
    
    .glass-panel {
        background: rgba(38, 42, 49, 0.4);
        backdrop-filter: blur(15px);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 12px;
        padding: 24px;
        margin-bottom: 20px;
    }

    .active-glow { box-shadow: 0 0 20px rgba(0, 242, 254, 0.15); border: 1px solid #00f2fe !important; }

    .stButton > button {
        background: linear-gradient(90deg, #00f2fe 0%, #00dce6 100%) !important;
        color: #00373a !important;
        font-weight: 800 !important;
        border-radius: 8px !important;
        border: none !important;
        height: 45px; width: 100%; transition: 0.3s;
    }
    
    .stButton > button:hover { box-shadow: 0 0 20px rgba(0, 242, 254, 0.4); transform: translateY(-2px); }
    .trust-val { color: #00f2fe; font-size: 64px; font-weight: 800; margin: 10px 0; }
    </style>
    """, unsafe_allow_html=True)