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

# --- 2. SESSION STATE MANAGEMENT ---
if 'view' not in st.session_state:
    st.session_state.view = "Intro"  # Navigation States: Intro, Dashboard, Rain, Flood, Satellite, Economic

# --- 3. UI STYLING & AI NEURONS BACKGROUND ---
st.set_page_config(page_title="AI Flood Prediction", layout="wide")

st.markdown("""
    <style>
    /* AI Neurons Background */
    .stApp {
        background: linear-gradient(rgba(0, 20, 40, 0.85), rgba(0, 20, 40, 0.85)), 
                    url("https://images.unsplash.com/photo-1677442136019-21780ecad995?auto=format&fit=crop&q=80&w=1920");
        background-size: cover; background-position: center; color: #fffdd0;
    }
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #000080 0%, #003366 100%) !important;
        border-right: 2px solid #fffdd0;
    }
    .info-box {
        background: rgba(0, 40, 80, 0.9); padding: 40px; border-radius: 25px;
        border: 2px solid #add8e6; box-shadow: 0px 15px 40px rgba(0,0,0,0.6);
        max-width: 1100px; margin: auto;
    }
    /* Welcome Button inside Info Box */
    .welcome-btn button {
        background-color: #add8e6 !important; color: #001f3f !important;
        font-weight: bold !important; font-size: 22px !important;
        border-radius: 12px !important; height: 70px !important; width: 100% !important;
        border: 2px solid #fffdd0 !important;
    }
    /* Dashboard Buttons Style */
    .db-btn button {
        width: 100% !important; height: 120px !important; border-radius: 10px 10px 0px 0px !important; 
        background: #112240 !important; color: #fffdd0 !important; border: 4px solid #003366 !important;
        font-weight: bold !important; box-shadow: 0px 8px 0px #000080 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 4. PAGE LOGIC ---

# PAGE 1: INTRODUCTORY FRONT PAGE
if st.session_state.view == "Intro":
    st.write("##")
    st.markdown('<h1 style="text-align:center; font-size: 55px; color:#add8e6; text-shadow: 2px 2px 10px #000;">AI FLOOD PREDICTION MODEL</h1>', unsafe_allow_html=True)
    st.write("##")
    
    st.markdown('<div class="info-box">', unsafe_allow_html=True)
    col_text, col_action = st.columns([2.5, 1])
    
    with col_text:
        st.markdown(f"""
            <h2 style="color:#add8e6; margin-bottom: 0px;">International Islamic University Islamabad</h2>
            <p style="font-size: 20px;"><b>Department:</b> BE.tech AI (Electrical and Computer Engineering)</p>
            <p style="font-size: 20px;"><b>Professor:</b> Engr. Asad</p>
            <hr style="border: 0.5px solid #add8e6; opacity: 0.3;">
            <p style="font-size: 18px; margin-bottom: 5px;"><b>Team Members:</b> Amna Mudassar Ali, Fatima Arshad, Ayesha Bint e Israr, Tehreen Ramesha</p>
            <p style="font-size: 18px;"><b>Roll Numbers:</b> 016809, 012221, 012214, 012218</p>
        """, unsafe_allow_html=True)
        
    with col_action:
        st.write("##")
        st.write("##")
        st.markdown('<div class="welcome-btn">', unsafe_allow_html=True)
        if st.button("WELCOME"):
            st.session_state.view = "Dashboard"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# PAGE 2: DASHBOARD (4 BUTTONS)
elif st.session_state.view == "Dashboard":
    st.markdown('<h1 style="text-align:center; font-size: 50px; color:#add8e6;">AI FLOOD PREDICTION MODEL</h1>', unsafe_allow_html=True)
    st.write("##")
    
    cols = st.columns(4)
    btn_data = [("EARLY RAIN\nPREDICTION", "Rain"), ("FLOOD RISK\nANALYSIS", "Flood"), 
                ("SATELLITE\nMONITORING", "Satellite"), ("ECONOMIC\nIMPACT", "Economic")]
    
    for i, (name, target) in enumerate(btn_data):
        with cols[i]:
            st.markdown('<div class="db-btn">', unsafe_allow_html=True)
            if st.button(f"🖥️\n{name}", key=f"dash_{i}"):
                st.session_state.view = target
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

# PAGE 3: DETAILED ANALYSIS PAGES
else:
    with st.sidebar:
        st.markdown("### SYSTEM CONTROL")
        if st.button("⬅️ DASHBOARD"):
            st.session_state.view = "Dashboard"
            st.rerun()
        if st.button("🏠 MAIN PAGE"):
            st.session_state.view = "Intro"
            st.rerun()
        st.write("---")
        selected_city = st.selectbox("TARGET AREA", list(LOCATIONS_PK.keys()))

    st.markdown(f"## 🛰️ Monitored Feed: {selected_city} - {st.session_state.view}")
    
    # Graphs with BLACK LINE
    y_data = np.random.randint(30, 95, 24)
    fig = px.line(x=list(range(24)), y=y_data, title=f"Real-time {st.session_state.view} Analysis")
    fig.update_traces(line_color='black', line_width=3)
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(255,255,255,0.1)', font_color="#fffdd0")
    st.plotly_chart(fig, use_container_width=True)

    if st.session_state.view == "Satellite":
        st.map(pd.DataFrame({'lat': [LOCATIONS_PK[selected_city][0]], 'lon': [LOCATIONS_PK[selected_city][1]]}))
