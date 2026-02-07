import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests

# --- 1. SET PAGE CONFIG ---
st.set_page_config(page_title="PAK-CLIMATE AI PRO", layout="wide", page_icon="🧪")

# --- 2. UI STYLING ---
st.markdown("""
    <style>
    .stApp {
        background: radial-gradient(circle at top right, #1a2a6c, #b21f1f, #fdbb2d);
        background-attachment: fixed;
        color: #e0e0e0;
    }
    .main-title {
        font-size: 45px !important;
        font-weight: 800;
        text-align: center;
        color: #ffffff;
        text-shadow: 0 0 10px #00ffcc;
        letter-spacing: 3px;
    }
    .metric-card {
        background: rgba(255, 255, 255, 0.1);
        padding: 20px;
        border-radius: 15px;
        backdrop-filter: blur(10px);
        text-align: center;
        border: 1px solid rgba(255,255,255,0.1);
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. DATASET ---
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
    st.markdown('<p class="main-title">PAK-CLIMATE AI PRO</p>', unsafe_allow_html=True)
    st.write("##")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button("🌧️ RAIN PREDICTION"):
            st.session_state.page = "Rain"; st.rerun()
    with col2:
        if st.button("🌊 FLOOD DYNAMICS"):
            st.session_state.page = "Flood"; st.rerun()
    with col3:
        if st.button("🛰️ SATELLITE INTEL"):
            st.session_state.page = "Satellite"; st.rerun()
    with col4:
        if st.button("📉 RECOVERY COST"):
            st.session_state.page = "Economic"; st.rerun()
else:
    # --- 5. DASHBOARD VIEW ---
    st.sidebar.button("⬅️ HOME", on_click=lambda: st.session_state.update({"page": "Home"}))
    selected_city = st.sidebar.selectbox("🎯 SELECT AREA", sorted(list(LOCATIONS.keys())))
    lat, lon = LOCATIONS[selected_city]

    @st.cache_data(ttl=600)
    def fetch_weather(lat, lon):
        url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true&hourly=temperature_2m,precipitation_probability&timezone=auto"
        return requests.get(url).json()

    data = fetch_weather(lat, lon)

    if data:
        st.markdown(f'<h2 style="color:white;">Operational Intel: {selected_city}</h2>', unsafe_allow_html=True)
        
        curr = data['current_weather']
        rain_val = data['hourly']['precipitation_probability'][0]
        
        c1, c2, c3 = st.columns(3)
        with c1: st.markdown(f'<div class="metric-card">🌡️ TEMP<h3>{curr["temperature"]}°C</h3></div>', unsafe_allow_html=True)
        with c2: st.markdown(f'<div class="metric-card">💨 WIND<h3>{curr["windspeed"]}kph</h3></div>', unsafe_allow_html=True)
        with c3: st.markdown(f'<div class="metric-card">💧 RAIN<h3>{rain_val}%</h3></div>', unsafe_allow_html=True)

        st.write("---")
        
        if st.session_state.page == "Rain":
            fig = px.line(x=data['hourly']['time'][:24], y=data['hourly']['precipitation_probability'][:24], 
                          title="24h Rain Probability", markers=True)
            st.plotly_chart(fig, use_container_width=True)
        
        elif st.session_state.page == "Flood":
            st.subheader("Flood Risk Gauge")
            fig = go.Figure(go.Indicator(
                mode = "gauge+number", value = rain_val,
                gauge = {'axis': {'range': [None, 100]}, 'bar': {'color': "#00ffcc"}}
            ))
            st.plotly_chart(fig, use_container_width=True)

        st.map(pd.DataFrame({'lat': [lat], 'lon': [lon]}))
    else:
        st.error("System Error: Unable to fetch data.")
