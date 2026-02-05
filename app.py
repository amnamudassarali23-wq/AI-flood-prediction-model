import streamlit as st
import pandas as pd
import plotly.express as px
import requests

st.set_page_config(page_title="AU Regional Monitor", layout="wide")

# Data for 48 locations
LOCATIONS = {
    "Sydney": [-33.86, 151.20], "Melbourne Airport": [-37.66, 144.84], "Brisbane": [-27.46, 153.02],
    "Perth": [-31.95, 115.86], "Adelaide": [-34.92, 138.60], "Hobart": [-42.88, 147.32],
    "Darwin": [-12.46, 130.84], "Canberra": [-35.28, 149.13], "Uluru": [-25.34, 131.03],
    "Alice Springs": [-23.69, 133.88], "Newcastle": [-32.92, 151.78], "Gold Coast": [-28.01, 153.40],
    "Cairns": [-16.91, 145.77], "Townsville": [-19.25, 146.81], "Wollongong": [-34.42, 150.89],
    "Albury": [-36.07, 146.91], "Wagga Wagga": [-35.10, 147.35], "Mildura": [-34.20, 142.12],
    "Bendigo": [-36.75, 144.27], "Ballarat": [-37.56, 143.85], "Woomera": [-31.19, 136.83],
    "Albany": [-35.02, 117.88], "Norfolk Island": [-29.04, 167.95], "Cobar": [-31.49, 145.83]
    # ... (Add remaining coordinates from previous list)
}

st.title("🇦🇺 Australia Regional Dashboard")
city = st.sidebar.selectbox("Select Location", sorted(LOCATIONS.keys()))
lat, lon = LOCATIONS[city]

@st.cache_data(ttl=600)
def get_data(lat, lon):
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true&hourly=temperature_2m"
    return requests.get(url).json()

res = get_data(lat, lon)
st.metric("Current Temperature", f"{res['current_weather']['temperature']}°C")

df = pd.DataFrame({"Time": res['hourly']['time'][:24], "Temp": res['hourly']['temperature_2m'][:24]})
st.plotly_chart(px.line(df, x="Time", y="Temp", title=f"24h Trend for {city}"))
st.map(pd.DataFrame([{"lat": lat, "lon": lon}]))
