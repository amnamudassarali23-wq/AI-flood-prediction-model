import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests
from datetime import datetime

# --- 1. SET PAGE CONFIG ---
st.set_page_config(page_title="PAK-CLIMATE AI PRO", layout="wide", page_icon="🧪")

# --- 2. THE ULTIMATE UI STYLING ---
st.markdown("""
    <style>
    /* Dark Theme Base */
    .stApp {
        background: radial-gradient(circle at top right, #1a2a6c, #b21f1f, #fdbb2d);
        background-attachment: fixed;
        color: #e0e0e0;
    }
    
    /* Header Animation */
    @keyframes glow {
        0% { text-shadow: 0 0 5px #00ffcc; }
        50% { text-shadow: 0 0 20px #00ffcc, 0 0 30px #00ffcc; }
        100% { text-shadow: 0 0 5px #00ffcc; }
    }
    
    .main-title {
        font-size: 50px !important;
        font-weight: 800;
        text-align: center;
        color: #ffffff;
        animation: glow 3s infinite;
        letter-spacing: 5px;
    }

    /* Glassmorphic Cards */
    .metric-card {
        background: rgba(255, 255, 255, 0.07);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 25px;
        border-radius: 20px;
        backdrop-filter: blur(15px);
        text-align: center;
        transition: transform 0.3s;
    }
    .metric-card:hover {
        transform: translateY(-5px);
        border-color: #00ffcc;
    }

    /* Professional Button Grid */
    .stButton>button {
        width: 100%;
        border-radius: 15px;
        height: 100px;
        background: rgba(0, 0, 0, 0.4);
        color: #00ffcc;
        border: 1px solid #00ffcc;
        font-size: 20px;
        font-weight: bold;
        transition: 0.4s;
        text-transform: uppercase;
    }
    .stButton>button:hover {
        background: #00ffcc;
        color: #000;
        box-shadow: 0 0 25px #00ffcc;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. DATA & STATE ---
LOCATIONS = {
    "Islamabad": [33.6844, 73.0479], "Karachi": [24.8607, 67.0011],
    "Lahore": [31.5204, 74.3587], "Jhelum": [32.9405, 73.7276],
    "Rawalpindi": [33.5651, 73.0169], "Faisalabad": [31.4504, 73.1350],
    "Quetta": [30.1798, 66.9750], "Gilgit": [35.9208, 74.3089]
}

if 'page' not in st.session_state:
    st.session_state.page = "Home"

# --- 4. NAVIGATION ---
if st.session_state.page == "Home":
    st.markdown('<p
