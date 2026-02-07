import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import requests
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder

# --- 1. COORDINATES FOR 37 PAKISTANI CITIES ---
LOCATIONS_PK = {
    "Karachi": [24.86, 67.00], "Lahore": [31.52, 74.35], "Faisalabad": [31.45, 73.13], 
    "Rawalpindi": [33.60, 73.04], "Gujranwala": [32.18, 74.19], "Peshawar": [34.01, 71.52], 
    "Multan": [30.15, 71.45], "Hyderabad": [25.39, 68.37], "Islamabad": [33.68, 73.04], 
    "Quetta": [30.17, 66.97], "Sargodha": [32.08, 72.67], "Sialkot": [32.49, 74.52], 
    "Bahawalpur": [29.35, 71.69], "Sukkur": [27.72, 68.82], "Jhang": [31.27, 72.33], 
    "Sheikhupura": [31.71, 73.98], "Rahim Yar Khan": [28.42, 70.29], "Dera Ghazi Khan": [30.04, 70.63], 
    "Gujrat": [32.57, 74.07], "Sahiwal": [30.66, 73.11], "Wah": [33.77, 72.75], 
    "Mardan": [34.19, 72.04], "Kasur": [31.11, 74.45], "Okara": [30.81, 73.45], 
    "Mingora": [34.77, 72.36], "Nawabshah": [26.24, 68.41], "Chiniot": [31.72, 72.97], 
    "Kotri": [25.37, 68.31], "Kamoke": [32.01, 74.22], "Hafizabad": [32.06, 73.68], 
    "Sadiqabad": [28.31, 70.13], "Mirpur Khas": [25.52, 69.01], "Burewala": [30.15, 72.68], 
    "Kohat": [33.58, 71.44], "Khanewal": [30.30, 71.93], "Dera Ismail Khan": [31.83, 70.90], 
    "Muzaffargarh": [30.07, 71.19]
}

# --- 2. SESSION STATE ---
if 'flow' not in st.session_state: st.session_state.flow = "Intro"
if 'page' not in st.session_state: st.session_state.page = "Home"

# --- 3. UI STYLING ---
st.set_page_config(page_title="AI Flood Prediction", layout="wide")

# AI Background and Styling
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(rgba(0, 31, 63, 0.85), rgba(0, 31, 63, 0.85)), 
                    url("https://images.unsplash.com/photo-1677442136019-21780ecad995?q=80&w=2000&auto=format&fit=crop");
        background-size: cover;
        background-attachment: fixed;
        color: #fffdd0;
    }
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #000080 0%, #003366 100%) !important;
        border-right: 2px solid #fffdd0;
    }
    .main-card {
        background: rgba(0, 51, 102, 0.8); padding: 30px; border-radius: 20px;
        border: 2px solid #add8e6; text-align: left;
        box-shadow: 0px 10px 30px rgba(0,0,0,0.5);
    }
    /* Welcome Button Styling */
    .stButton>button {
        background: #add8e6 !important; color: #001f3f !important;
        font-weight: bold !important; font-size: 20px !important;
        border-radius: 10px !important; border: 2px solid #fffdd0 !important;
        height: 60px !important; width: 100% !important;
        transition: 0.3s;
    }
    .dashboard-btn>div>button {
        height: 120px !important; background: #112240 !important; color: #fffdd0 !important;
        border-radius: 10px 10px 0px 0px !important; border: 4px solid #003366 !important;
        box-shadow: 0px 8px 0px #000080 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 4. PAGE LOGIC ---

# PAGE 1: INTRODUCTORY FRONT PAGE
if st.session_state.flow == "Intro":
    st.write("##")
    st.markdown('<h1 style="text-align:center; font-size: 55px; color:#add8e6; text-shadow: 2px 2px 10px #000;">AI FLOOD PREDICTION MODEL</h1>', unsafe_allow_html=True)
    st.write("##")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown(f"""
        <div class="main-card">
            <h3 style="color:#add8e6; border-bottom: 2px solid #add8e6;">INSTITUTIONAL DETAILS</h3>
            <p style="font-size: 19px; margin-top:15px;"><b>University:</b> International Islamic University Islamabad</p>
            <p style="font-size: 19px;"><b>Department:</b> BE.tech AI (Electrical and Computer Engineering)</p>
            <p style="font-size: 19px;"><b>Professor:</b> Engr. Asad</p>
            <hr style="opacity: 0.2;">
            <p style="font-size: 17px;"><b>Team:</b> Amna Mudassar Ali, Fatima Arshad, Ayesha Bint e Israr, Tehreen Ramesha</p>
            <p style="font-size: 17px;"><b>Roll No:</b> 016809, 012221, 012214, 012218</p>
        </div>
        """, unsafe_allow_html=True)
        
    with col2:
        st.write("##")
        st.write("##")
        st.write("##")
        if st.button("WELCOME"):
            st.session_state.flow = "Dashboard"
            st.rerun()

# PAGE 2: DASHBOARD
elif st.session_state.flow == "Dashboard" and st.session_state.page == "Home":
    st.markdown('<h1 style="text-align:center; font-size: 45px;">AI FLOOD PREDICTION MODEL</h1>', unsafe_allow_html=True)
    st.write("---")
    cols = st.columns(4)
    btn_data = [("EARLY RAIN\nPREDICTION", "Rain"), ("FLOOD RISK\nANALYSIS", "Flood"), 
                ("SATELLITE\nMONITORING", "Satellite"), ("ECONOMIC\nIMPACT", "Economic")]
    for i, (name, pg) in enumerate(btn_data):
        with cols[i]:
            st.markdown('<div class="dashboard-btn">', unsafe_allow_html=True)
            if st.button(f"🖥️\n{name}"):
                st.session_state.page = pg; st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

# PAGE 3: FEATURE PAGES
else:
    with st.sidebar:
        st.markdown("### SYSTEM CONTROL")
        if st.button("⬅️ DASHBOARD"): st.session_state.page = "Home"; st.rerun()
        if st.button("🏠 MAIN PAGE"): st.session_state.flow = "Intro"; st.rerun()
        st.write("---")
        city = st.selectbox("TARGET AREA", list(LOCATIONS_PK.keys()))
    
    st.markdown(f"## 🛰️ Monitored Feed: {city}")
    # Graph logic with black line
    y_data = np.random.randint(30, 90, 24)
    fig = px.line(x=list(range(24)), y=y_data, title="Live Atmospheric Saturation")
    fig.update_traces(line_color='black', line_width=3)
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(255,255,255,0.2)', font_color="#fffdd0")
    st.plotly_chart(fig, use_container_width=True)
