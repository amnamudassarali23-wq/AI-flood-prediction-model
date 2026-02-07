import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests

# --- 1. SET PAGE CONFIG ---
st.set_page_config(page_title="AI Flood prediction model", layout="wide", page_icon="📡")

# --- 2. THEME STYLING ---
st.markdown("""
    <style>
    .stApp {
        background-color: #001f3f; 
        color: #fffdd0; /* Cream Text */
    }
    
    h1, h2, h3, p, span, label {
        color: #fffdd0 !important;
    }

    /* Computer-Shaped Buttons */
    .stButton>button {
        width: 100%;
        height: 120px;
        border-radius: 10px 10px 0px 0px; 
        background: #112240;
        color: #fffdd0;
        border: 4px solid #add8e6; /* Light Blue Border */
        font-weight: bold;
        box-shadow: 0px 10px 0px #00008B; 
        transition: 0.3s;
        font-size: 18px;
    }
    .stButton>button:hover {
        background: #add8e6;
        color: #001f3f;
        transform: translateY(-5px);
    }

    /* Light Blue Selection Box */
    div[data-baseweb="select"] > div {
        background-color: #add8e6 !important; 
        border-radius: 8px !important;
        border: 2px solid #fffdd0 !important;
        color: #001f3f !important;
    }

    .metric-card {
        background: rgba(173, 216, 230, 0.1);
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        border: 1px solid #add8e6;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. DATA & STATE ---
LOCATIONS = {
    "Islamabad": [33.6844, 73.0479], "Karachi": [24.8607, 67.0011],
    "Lahore": [31.5204, 74.3587], "Jhelum": [32.9405, 73.7276],
    "Quetta": [30.1798, 66.9750], "Gilgit": [35.9208, 74.3089]
}

if 'page' not in st.session_state:
    st.session_state.page = "Home"

# --- 4. MAIN INTERFACE (Computer Box Buttons) ---
if st.session_state.page == "Home":
    st.markdown('<h1 style="text-align:center;">AI FLOOD PREDICTION MODEL</h1>', unsafe_allow_html=True)
    st.write("##")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button("🖥️\nEARLY RAIN\nPREDICTION"):
            st.session_state.page = "Rain"; st.rerun()
    with col2:
        if st.button("🖥️\nFLOOD RISK\nANALYSIS"):
            st.session_state.page = "Flood"; st.rerun()
    with col3:
        if st.button("🖥️\nSATELLITE\nMONITORING"):
            st.session_state.page = "Satellite"; st.rerun()
    with col4:
        if st.button("🖥️\nECONOMIC\nIMPACT"):
            st.session_state.page = "Economic"; st.rerun()

else:
    # --- 5. OPERATIONAL DASHBOARD ---
    with st.sidebar:
        st.markdown("<h3 style='color:#add8e6;'>CONTROL PANEL</h3>", unsafe_allow_html=True)
        if st.button("⬅️ BACK TO SYSTEM"):
            st.session_state.page = "Home"; st.rerun()
        st.write("---")
        # City selection box (styled Light Blue)
        selected_city = st.selectbox("TARGET AREA", list(LOCATIONS.keys()))
    
    lat, lon = LOCATIONS[selected_city]

    @st.cache_data(ttl=600)
    def fetch_weather(lat, lon):
        try:
            url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true&hourly=temperature_2m,precipitation_probability&timezone=auto"
            return requests.get(url).json()
        except: return None

    data = fetch_weather(lat, lon)

    if data:
        st.markdown(f"## 📍 Operational Feed: {selected_city}")
        
        rain_val = data['hourly']['precipitation_probability'][0]
        c1, c2, c3 = st.columns(3)
        with c1: st.markdown(f'<div class="metric-card">TEMPERATURE<h3>{data["current_weather"]["temperature"]}°C</h3></div>', unsafe_allow_html=True)
        with c2: st.markdown(f'<div class="metric-card">RAIN PROB.<h3>{rain_val}%</h3></div>', unsafe_allow_html=True)
        with c3: st.markdown(f'<div class="metric-card">WIND SPEED<h3>{data["current_weather"]["windspeed"]}kph</h3></div>', unsafe_allow_html=True)

        st.write("---")
        
        # Simple Map logic
        map_df = pd.DataFrame({'lat': [lat], 'lon': [lon]})
        st.map(map_df)
    else:
        st.error("Error connecting to weather satellite.")
