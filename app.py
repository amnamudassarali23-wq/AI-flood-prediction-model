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

# --- 2. AI ENGINE ---
RAW_DATA = [{'Rainfall': 0.0, 'Humidity': 50, 'Pressure': 1010, 'Target': 0}, {'Rainfall': 20.0, 'Humidity': 90, 'Pressure': 990, 'Target': 1}]
@st.cache_resource
def build_ai():
    df = pd.DataFrame(RAW_DATA * 50)
    le = LabelEncoder()
    le.fit(list(LOCATIONS_PK.keys()))
    model = RandomForestClassifier().fit(np.random.rand(100, 8), np.random.randint(0, 2, 100))
    return model, le
ai_model, label_encoder = build_ai()

# --- 3. UI STYLING ---
st.set_page_config(page_title="AI Flood Prediction", layout="wide")
st.markdown("""
    <style>
    .stApp { background-color: #001f3f; color: #fffdd0; }
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #000080 0%, #003366 100%) !important;
        border-right: 2px solid #fffdd0;
    }
    .main-card {
        background: rgba(0, 51, 102, 0.6); padding: 40px; border-radius: 25px;
        border: 3px solid #add8e6; text-align: center; margin: auto; max-width: 900px;
        box-shadow: 0px 15px 35px rgba(0,0,0,0.7);
    }
    .start-btn button {
        background: #add8e6 !important; color: #001f3f !important;
        font-weight: bold !important; font-size: 24px !important;
        padding: 20px 50px !important; border-radius: 15px !important;
        width: 300px !important; height: 80px !important;
    }
    .stButton>button {
        width: 100%; height: 120px; border-radius: 10px 10px 0px 0px; 
        background: #112240; color: #fffdd0; border: 4px solid #003366;
        font-weight: bold; box-shadow: 0px 8px 0px #000080;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 4. SESSION STATE ---
if 'flow' not in st.session_state: st.session_state.flow = "Intro"
if 'page' not in st.session_state: st.session_state.page = "Home"

# --- 5. PAGE LOGIC ---

# PAGE 1: INTRODUCTORY FRONT PAGE
if st.session_state.flow == "Intro":
    st.write("##")
    st.markdown(f"""
    <div class="main-card">
        <h1 style="color:#add8e6; font-size: 45px;">AI FLOOD PREDICTION SYSTEM</h1>
        <p style="font-size: 20px; opacity: 0.8;">Final Year Project Development</p>
        <hr style="border: 1px solid #add8e6; opacity: 0.2;">
        <h3 style="color:#fffdd0;">International Islamic University Islamabad</h3>
        <p style="font-size: 18px;"><b>Department:</b> BE.tech AI (Electrical and Computer Engineering)</p>
        <p style="font-size: 18px;"><b>Professor:</b> Engr. Asad</p>
        <div style="background: rgba(0,0,0,0.2); padding: 20px; border-radius: 15px; margin: 20px 0;">
            <p><b>Team Members:</b> Amna Mudassar Ali, Fatima Arshad, Ayesha Bint e Israr, Tehreen Ramesha</p>
            <p><b>Roll Numbers:</b> 016809, 012221, 012214, 012218</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.write("##")
    col1, col2, col3 = st.columns([1,1,1])
    with col2:
        st.markdown('<div class="start-btn">', unsafe_allow_html=True)
        if st.button("LET'S START"):
            st.session_state.flow = "Dashboard"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# PAGE 2: PREVIOUS 4-BUTTON FRONT PAGE
elif st.session_state.flow == "Dashboard" and st.session_state.page == "Home":
    st.markdown('<h1 style="text-align:center;">SYSTEM DASHBOARD</h1>', unsafe_allow_html=True)
    st.write("##")
    cols = st.columns(4)
    btn_data = [("EARLY RAIN\nPREDICTION", "Rain"), ("FLOOD RISK\nANALYSIS", "Flood"), 
                ("SATELLITE\nMONITORING", "Satellite"), ("ECONOMIC\nIMPACT", "Economic")]
    for i, (name, pg) in enumerate(btn_data):
        with cols[i]:
            if st.button(f"🖥️\n{name}"):
                st.session_state.page = pg; st.rerun()

# PAGE 3: FEATURE PAGES
else:
    with st.sidebar:
        st.markdown("### SYSTEM CONTROL")
        if st.button("⬅️ DASHBOARD"): st.session_state.page = "Home"; st.rerun()
        if st.button("🏠 MAIN PAGE"): st.session_state.flow = "Intro"; st.rerun()
        st.write("---")
        city = st.selectbox("TARGET AREA", list(LOCATIONS_PK.keys()))
    
    st.markdown(f"## 🛰️ Monitored Feed: {city}")
    # Graphs remain with black line as requested
    fig = px.line(x=list(range(24)), y=np.random.randint(40, 90, 24))
    fig.update_traces(line_color='black')
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(255,255,255,0.1)', font_color="#fffdd0")
    st.plotly_chart(fig, use_container_width=True)
