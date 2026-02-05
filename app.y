import streamlit as st
import pandas as pd
import plotly.express as px
import requests
from datetime import datetime

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(page_title="AU Regional Monitor", layout="wide", page_icon="🇦🇺")

# --- 2. DATA SOURCE (48 LOCATIONS) ---
# Organized for the dashboard layout
AU_LOCATIONS = {
    "New South Wales": {
        "Sydney": [-33.8688, 151.2093], "Sydney Airport": [-33.9399, 151.1753], 
        "Newcastle": [-32.9283, 151.7817], "Wollongong": [-34.4278, 150.8931],
        "Penrith": [-33.7507, 150.6942], "Richmond": [-33.5992, 150.7500],
        "Badgerys Creek": [-33.8884, 150.7514], "Coffs Harbour": [-30.2963, 153.1135],
        "Albury": [-36.0737, 146.9135], "Wagga Wagga": [-35.1082, 147.3598],
        "Moree": [-29.4658, 149.8417], "Cobar": [-31.4997, 145.8319],
        "Norah Head": [-33.2817, 151.5767], "Williamtown": [-32.7936, 151.8403]
    },
    "Victoria": {
        "Melbourne Airport": [-37.6690, 144.8410], "Ballarat": [-37.5622, 143.8503],
        "Bendigo": [-36.7570, 144.2794], "Sale": [-38.1052, 147.0678],
        "Mildura": [-34.2080, 142.1246], "Nhill": [-36.3333, 141.6500],
        "Portland": [-38.3463, 141.6042], "Watsonia": [-37.7083, 145.0833],
        "Dartmoor": [-37.9167, 141.2833]
    },
    "Queensland": {
        "Brisbane": [-27.4698, 153.0251], "Gold Coast": [-28.0167, 153.4000],
        "Cairns": [-16.9186, 145.7781], "Townsville": [-19.2590, 146.8169]
    },
    "Western Australia": {
        "Perth": [-31.9505, 115.8605], "Perth Airport": [-31.9403, 115.9668],
        "Albany": [-35.0269, 117.8814], "Witchcliffe": [-34.0261, 115.1000],
        "Pearce RAAF": [-31.6676, 116.0292], "Salmon Gums": [-32.9814, 121.6438],
        "Walpole": [-34.9777, 116.7338]
    },
    "South Australia": {
        "Adelaide": [-34.9285, 138.6007], "Mount Gambier": [-37.8284, 140.7804],
        "Nuriootpa": [-34.4691, 138.9939], "Woomera": [-31.1998, 136.8322]
    },
    "ACT & Others": {
        "Canberra": [-35.2809, 149.1300], "Tuggeranong": [-35.4244, 149.0888],
        "Mount Ginini": [-35.5294, 148.7722], "Norfolk Island": [-29.0408, 167.9547],
        "Hobart": [-42.8821, 147.3272], "Launceston": [-41.4332, 147.1441],
        "Alice Springs": [-23.6980, 133.8807], "Darwin": [-12.4634, 130.8456],
        "Katherine": [-14.4652, 132.2635], "Uluru": [-25.3444, 131.0369]
    }
}

# Flatten for mapping
flat_list = []
for state, cities in AU_LOCATIONS.items():
    for city, coords in cities.items():
        flat_list.append({"City": city, "State": state, "lat": coords[0], "lon": coords[1]})
df_all = pd.DataFrame(flat_list)

# --- 3. SIDEBAR NAVIGATION ---
st.sidebar.title("🔍 Filter Dashboard")
selected_state = st.sidebar.selectbox("Select State/Region", list(AU_LOCATIONS.keys()))
selected_city = st.sidebar.selectbox("Select Specific Location", list(AU_LOCATIONS[selected_state].keys()))

# Get Lat/Lon for API call
lat, lon = AU_LOCATIONS[selected_state][selected_city]

# --- 4. FETCH LIVE API DATA ---
@st.cache_data(ttl=300)
def fetch_weather(lat, lon):
    api_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true&hourly=temperature_2m,relative_humidity_2m,wind_speed_10m&timezone=auto"
    return requests.get(api_url).json()

data = fetch_weather(lat, lon)
current = data['current_weather']

# --- 5. MAIN DASHBOARD LAYOUT ---
st.title(f"📊 Dashboard: {selected_city}, {selected_state}")
st.markdown(f"**Last Updated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# KPI Metrics
m1, m2, m3, m4 = st.columns(4)
m1.metric("Temperature", f"{current['temperature']}°C")
m2.metric("Wind Speed", f"{current['windspeed']} km/h")
m3.metric("Latitude", f"{lat}")
m4.metric("Longitude", f"{lon}")

st.divider()

# Left Column: Map | Right Column: Chart
col_left, col_right = st.columns([1, 1])

with col_left:
    st.subheader("📍 Location Map")
    # Plotly Map showing the selected point
    fig_map = px.scatter_mapbox(df_all, lat="lat", lon="lon", hover_name="City", 
                                color="State", zoom=3, height=450)
    fig_map.update_layout(mapbox_style="open-street-map", margin={"r":0,"t":0,"l":0,"b":0})
    # Highlight the selected city
    fig_map.add_trace(px.scatter_mapbox(pd.DataFrame([{"lat": lat, "lon": lon}]), 
                                        lat="lat", lon="lon").data[0])
    st.plotly_chart(fig_map, use_container_width=True)

with col_right:
    st.subheader("📈 24h Temperature Trend")
    hourly_data = pd.DataFrame({
        "Time": pd.to_datetime(data['hourly']['time'][:24]),
        "Temp": data['hourly']['temperature_2m'][:24]
    })
    fig_trend = px.line(hourly_data, x="Time", y="Temp", markers=True)
    fig_trend.update_layout(xaxis_title="", yaxis_title="Temp (°C)")
    st.plotly_chart(fig_trend, use_container_width=True)

# --- 6. DATA TABLE ---
with st.expander("See Raw Data for all 48 Locations"):
    st.dataframe(df_all, use_container_width=True)
