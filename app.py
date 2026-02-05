import streamlit as st
import pandas as pd
import plotly.express as px
import requests
from datetime import datetime

# Page Configuration
st.set_page_config(page_title="PAKISTAN Weather Monitor", layout="wide")

# Correct Location Data (Sample of your 48 locations)
LOCATIONS = {
    "Islamabad": [-33.8688, 151.2093],
    "Karachi": [-37.6690, 144.8410],
    "Lahore": [-27.4698, 153.0251],
    "Jehlum": [-31.9505, 115.8605],
    "Rawal pindi": [-34.9285, 138.6007],
    "Faisalabad": [-25.3444, 131.0369],
    "Balochistan": [-23.6980, 133.8807],
    "Gilgit": [-12.4634, 130.8456]
}

st.title("📍PAKISTAN Weather Dashboard")

# Sidebar
selected_city = st.sidebar.selectbox("Select a Location", sorted(LOCATIONS.keys()))
lat, lon = LOCATIONS[selected_city]

# Fetch Data with Error Handling
@st.cache_data(ttl=600)
def get_weather_data(lat, lon):
    try:
        url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true&hourly=temperature_2m"
        response = requests.get(url)
        return response.json()
    except Exception as e:
        return None

data = get_weather_data(lat, lon)

if data and 'current_weather' in data:
    # Display Metrics
    curr = data['current_weather']
    col1, col2 = st.columns(2)
    col1.metric("Current Temp", f"{curr['temperature']}°C")
    col2.metric("Wind Speed", f"{curr['windspeed']} km/h")

    # Interactive Map
    st.subheader(f"Location Map: {selected_city}")
    map_data = pd.DataFrame({'lat': [lat], 'lon': [lon]})
    st.map(map_data)

    # Hourly Chart
    st.subheader("24-Hour Temperature Forecast")
    hourly_df = pd.DataFrame({
        "Time": pd.to_datetime(data['hourly']['time'][:24]),
        "Temp (°C)": data['hourly']['temperature_2m'][:24]
    })
    fig = px.line(hourly_df, x="Time", y="Temp (°C)", markers=True)
    st.plotly_chart(fig, use_container_width=True)
else:
    st.error("Weather data fetch karne mein masla aa raha hai. Internet check karein.")
