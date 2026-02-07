import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests
from datetime import datetime

# --- 1. SET PAGE CONFIG & THEME ---
st.set_page_config(page_title="PAK-CLIMATE AI", layout="wide", page_icon="⚡")

# --- 2. ADVANCED STYLING (GLASSMORPHISM) ---
st.markdown("""
    <style>
    /* Main background */
    .stApp {
        background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
        color: white;
    }
    /* Card-like containers */
    div[data-testid="stVerticalBlock"] > div:has(div.stButton) {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 15px;
        padding: 20px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
    }
    /* Metric styling */
    div[data-testid="stMetricValue"] {
        color: #00ffcc !important;
        font-size: 32px;
    }
    /* Button Hover Effects */
    .stButton>button {
        border-radius: 12px;
        height: 80px;
        border: 1px solid #00ffcc;
        background: transparent;
        color: white;
        font-size: 18px;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background: #00ffcc;
        color: #0f2027;
        box-shadow: 0px 0px 15px #00ffcc;
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

# Navigation State
if 'page' not in st.session_state:
    st.session_state.page = "Home"

# --- 4. NAVIGATION LOGIC ---
if st.session_state.page == "Home":
    st.title("⚡ PAK-CLIMATE INTELLIGENCE")
    st.write("### Select an AI Analysis Module")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("🌧️\nEarly Rain\nPrediction"):
            st.session_state.page = "Rain"
            st.rerun()
    with col2:
        if st.button("🌊\nFlood Risk\nAnalysis"):
            st.session_state.page = "Flood"
            st.rerun()
    with col3:
        if st.button("🛰️\nSatellite\nMonitoring"):
            st.session_state.page = "Satellite"
            st.rerun()
    with col4:
        if st.button("📉\nEconomic\nImpact"):
            st.session_state.page = "Economic"
            st.rerun()

else:
    # --- 5. DASHBOARD INTERFACE ---
    if st.sidebar.button("🔙 Back to Main Menu"):
        st.session_state.page = "Home"
        st.rerun()

    st.title(f"🔍 {st.session_state.page} Module")
    selected_city = st.sidebar.selectbox("Target City", list(LOCATIONS.keys()))
    lat, lon = LOCATIONS[selected_city]

    # Fetch Data
    @st.cache_data(ttl=600)
    def fetch_weather(lat, lon):
        url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true&hourly=temperature_2m,relative_humidity_2m,precipitation_probability,surface_pressure&timezone=auto"
        return requests.get(url).json()

    data = fetch_weather(lat, lon)

    if data:
        # --- METRIC CARDS ---
        curr = data['current_weather']
        rain_val = data['hourly']['precipitation_probability'][0]
        
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("TEMP", f"{curr['temperature']}°C")
        m2.metric("WIND", f"{curr['windspeed']} km/h")
        m3.metric("RAIN PROB", f"{rain_val}%")
        m4.metric("PRESSURE", f"{data['hourly']['surface_pressure'][0]} hPa")

        # --- DYNAMIC CONTENT BASED ON BUTTON ---
        st.markdown("---")
        
        if st.session_state.page == "Rain":
            st.subheader("⛈️ Precipitation Forecast")
            fig = px.area(x=data['hourly']['time'][:24], y=data['hourly']['precipitation_probability'][:24],
                          labels={'x': 'Time', 'y': 'Probability %'}, color_discrete_sequence=['#00ffcc'])
            st.plotly_chart(fig, use_container_width=True)

        elif st.session_state.page == "Flood":
            st.subheader("🌊 Flood Risk Assessment")
            risk_level = "LOW" if rain_val < 30 else "MEDIUM" if rain_val < 60 else "HIGH"
            st.info(f"The Current Flood Risk for {selected_city} is **{risk_level}** based on satellite moisture data.")
            # Gauge Chart for Flood Risk
            fig_gauge = go.Figure(go.Indicator(
                mode = "gauge+number", value = rain_val,
                title = {'text': "Saturation Level"},
                gauge = {'axis': {'range': [None, 100]}, 'bar': {'color': "#00ffcc"}}
            ))
            st.plotly_chart(fig_gauge)

        # --- MAP VIEW ---
        st.subheader(f"📍 Precision Mapping: {selected_city}")
        st.map(pd.DataFrame({'lat': [lat], 'lon': [lon]}), zoom=11)

    else:
        st.error("API Connection Lost.")
