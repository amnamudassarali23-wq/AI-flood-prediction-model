import streamlit as st
import pandas as pd
import plotly.express as px
import requests

# Page Configuration
st.set_page_config(page_title="PAKISTAN Weather Monitor", layout="wide")

# 1. Dataset changed from Australia to Pakistan
# 2. Locations updated with Pakistan cities and their correct coordinates
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

# Session state to keep track of button clicks
if 'show_interface' not in st.session_state:
    st.session_state.show_interface = False

st.title("📍 PAKISTAN Weather Dashboard")

# 3, 4, 5. Creating 4 buttons initially
st.subheader("Select a Service")
col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("Early Rain Prediction", use_container_width=True):
        st.session_state.show_interface = True
with col2:
    if st.button("Button 2", use_container_width=True):
        st.session_state.show_interface = True
with col3:
    if st.button("Button 3", use_container_width=True):
        st.session_state.show_interface = True
with col4:
    if st.button("Button 4", use_container_width=True):
        st.session_state.show_interface = True

# 6. Show interface only when a button is clicked
if st.session_state.show_interface:
    st.divider()
    
    # Sidebar for city selection
    selected_city = st.sidebar.selectbox("Select a Location", sorted(LOCATIONS.keys()))
    lat, lon = LOCATIONS[selected_city]

    # Fetch Data
    @st.cache_data(ttl=600)
    def get_weather_data(lat, lon):
        try:
            url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true&hourly=temperature_2m"
            response = requests.get(url)
            return response.json()
        except Exception:
            return None

    data = get_weather_data(lat, lon)

    if data and 'current_weather' in data:
        curr = data['current_weather']
        m1, m2 = st.columns(2)
        m1.metric("Current Temp", f"{curr['temperature']}°C")
        m2.metric("Wind Speed", f"{curr['windspeed']} km/h")

        # Map Interface
        st.subheader(f"Location Map: {selected_city}")
        map_data = pd.DataFrame({'lat': [lat], 'lon': [lon]})
        st.map(map_data)

        # Graph
        st.subheader("24-Hour Forecast")
        hourly_df = pd.DataFrame({
            "Time": pd.to_datetime(data['hourly']['time'][:24]),
            "Temp (°C)": data['hourly']['temperature_2m'][:24]
        })
        st.plotly_chart(px.line(hourly_df, x="Time", y="Temp (°C)", markers=True), use_container_width=True)
    else:
        st.error("Data fetch nahi ho raha. Internet check karein.")

    # Reset button to go back to the 4 buttons menu
    if st.sidebar.button("Back to Menu"):
        st.session_state.show_interface = False
        st.rerun()
