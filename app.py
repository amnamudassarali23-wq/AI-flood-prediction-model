import streamlit as st
import pandas as pd
import plotly.express as px
import requests
from datetime import datetime

# --- PAGE CONFIG ---
st.set_page_config(page_title="Pro Pakistan Weather", layout="wide", page_icon="🇵🇰")

# --- CUSTOM CSS FOR EFFECTIVENESS ---
st.markdown("""
    <style>
    .main { background-color: #f0f2f6; }
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        height: 4em;
        background-color: #0066cc;
        color: white;
        font-weight: bold;
        border: None;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #004499;
        border: 2px solid #ffffff;
    }
    </style>
    """, unsafe_allow_html=True)

# --- PAKISTAN DATASET ---
LOCATIONS = {
    "Islamabad": [33.6844, 73.0479],
    "Karachi": [24.8607, 67.0011],
    "Lahore": [31.5204, 74.3587],
    "Jhelum": [32.9405, 73.7276],
    "Rawalpindi": [33.5651, 73.0169],
    "Faisalabad": [31.4504, 73.1350],
    "Quetta": [30.1798, 66.9750],
    "Gilgit": [35.9208, 74.3089]
}

# Session State for App Navigation
if 'mode' not in st.session_state:
    st.session_state.mode = None

# --- HEADER ---
st.title("🇵🇰 Pakistan Climate Intelligence Dashboard")
st.markdown("---")

# --- NAVIGATION BUTTONS (The 4 Main Actions) ---
if st.session_state.mode is None:
    st.info("👋 Welcome! Please select a specialized service below to begin.")
    c1, c2, c3, c4 = st.columns(4)
    
    if c1.button("🌧️ Early Rain Prediction"):
        st.session_state.mode = "Rain Prediction"
        st.rerun()
    if c2.button("📊 Button 2"):
        st.session_state.mode = "B2"
        st.rerun()
    if c3.button("📡 Button 3"):
        st.session_state.mode = "B3"
        st.rerun()
    if c4.button("⚙️ Button 4"):
        st.session_state.mode = "B4"
        st.rerun()

# --- INTERFACE AFTER SELECTION ---
else:
    # Sidebar back button
    if st.sidebar.button("⬅️ Return to Home"):
        st.session_state.mode = None
        st.rerun()

    st.sidebar.header(f"Service: {st.session_state.mode}")
    city = st.sidebar.selectbox("Select Target City", sorted(LOCATIONS.keys()))
    lat, lon = LOCATIONS[city]

    # API Data Fetching with Extended Parameters
    @st.cache_data(ttl=600)
    def get_pro_data(lat, lon):
        url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true&hourly=temperature_2m,relative_humidity_2m,precipitation_probability,cloudcover&timezone=auto"
        return requests.get(url).json()

    data = get_pro_data(lat, lon)

    if data:
        # --- TOP LEVEL METRICS ---
        curr = data['current_weather']
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Temperature", f"{curr['temperature']}°C")
        m2.metric("Wind Speed", f"{curr['windspeed']} km/h")
        
        # Rain Logic for effectiveness
        rain_prob = data['hourly']['precipitation_probability'][0]
        m3.metric("Rain Probability", f"{rain_prob}%")
        
        humidity = data['hourly']['relative_humidity_2m'][0]
        m4.metric("Humidity", f"{humidity}%")

        # --- RAIN ANALYSIS (Specific to Button 1) ---
        if st.session_state.mode == "Rain Prediction":
            st.success(f"### 🎯 Intelligence Report for {city}")
            if rain_prob > 50:
                st.error("⚠️ HIGH RISK: Significant chance of rain detected within the next hour.")
            elif rain_prob > 20:
                st.warning("⚡ MODERATE: Overcast skies. Light showers possible.")
            else:
                st.info("☀️ STABLE: No rain expected in the immediate forecast.")

        # --- VISUALS SECTION ---
        col_map, col_chart = st.columns([1, 1.2])

        with col_map:
            st.subheader("📍 Geospatial View")
            map_df = pd.DataFrame({'lat': [lat], 'lon': [lon]})
            st.map(map_df, zoom=10)

        with col_chart:
            st.subheader("📉 24-Hour Trend Analysis")
            chart_df = pd.DataFrame({
                "Time": pd.to_datetime(data['hourly']['time'][:24]),
                "Temperature (°C)": data['hourly']['temperature_2m'][:24],
                "Rain Prob (%)": data['hourly']['precipitation_probability'][:24]
            })
            # Multi-line chart for effectiveness
            fig = px.line(chart_df, x="Time", y=["Temperature (°C)", "Rain Prob (%)"], 
                          markers=True, template="plotly_white")
            st.plotly_chart(fig, use_container_width=True)

    else:
        st.error("Connectivity Issue: Failed to retrieve data from Open-Meteo API.")
