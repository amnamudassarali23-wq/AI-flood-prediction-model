import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests

# --- 1. SET PAGE CONFIG ---
st.set_page_config(page_title="AI Flood prediction model", layout="wide", page_icon="📡")

# --- 2. CUSTOM CSS: NAVY, DARK BLUE, LIGHT BLUE & CREAM ---
st.markdown("""
    <style>
    /* Navy Blue Base */
    .stApp {
        background-color: #001f3f; 
        color: #f8f1e5;
    }
    
    /* Dark Blue Headings with Subtle Glow */
    .main-title {
        font-size: 42px !important;
        font-weight: 800;
        text-align: center;
        color: #00008B; /* Dark Blue */
        text-shadow: 1px 1px 10px rgba(0, 0, 139, 0.3);
        padding: 20px;
        animation: fadeIn 3s ease-in;
    }
    
    h1, h2, h3 {
        color: #00008B !important;
    }

    /* Cream Colored Circle/Rounded Box for City Selection */
    div[data-baseweb="select"] > div {
        background-color: #fffdd0 !important; /* Cream Color */
        border-radius: 50px !important; /* Circle/Rounded Shape */
        border: 2px solid #00008B !important;
        color: #001f3f !important;
    }

    /* Light Blue Metric Cards */
    .metric-card {
        background: rgba(173, 216, 230, 0.15); /* Very Light Blue Transparency */
        padding: 20px;
        border-radius: 20px;
        text-align: center;
        border: 1px solid #add8e6;
        transition: 0.5s;
    }
    .metric-card:hover {
        background: rgba(173, 216, 230, 0.25);
        transform: scale(1.02);
    }

    /* Sidebar Navy Theme */
    [data-testid="stSidebar"] {
        background-color: #001329 !important;
        border-right: 1px solid #00008B;
    }

    /* Subtle Animation */
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    
    /* Navigation Buttons */
    .stButton>button {
        border-radius: 30px;
        background-color: #00008B;
        color: white;
        border: none;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #add8e6;
        color: #00008B;
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

# --- 4. NAVIGATION ---
if st.session_state.page == "Home":
    st.markdown('<p class="main-title">AI FLOOD PREDICTION MODEL</p>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    modules = [("🌧️ RAIN", "Rain"), ("🌊 FLOOD", "Flood"), ("🛰️ INTEL", "Satellite"), ("📉 COST", "Economic")]
    
    for i, (label, target) in enumerate(modules):
        with [col1, col2, col3, col4][i]:
            if st.button(label):
                st.session_state.page = target
                st.rerun()
else:
    # --- 5. DASHBOARD ---
    with st.sidebar:
        st.write("### COMMAND CENTER")
        if st.button("⬅️ BACK TO MENU"):
            st.session_state.page = "Home"
            st.rerun()
        st.write("---")
        # Circle/Cream selection box is styled via CSS above
        selected_city = st.selectbox("CHOOSE TARGET LOCATION", list(LOCATIONS.keys()))

    lat, lon = LOCATIONS[selected_city]

    @st.cache_data(ttl=600)
    def fetch_weather(lat, lon):
        url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true&hourly=temperature_2m,precipitation_probability&timezone=auto"
        return requests.get(url).json()

    data = fetch_weather(lat, lon)

    if data:
        st.markdown(f'<h2 style="text-align:center;">Analyzing: {selected_city}</h2>', unsafe_allow_html=True)
        
        # Metrics with Light Blue cards
        rain_val = data['hourly']['precipitation_probability'][0]
        c1, c2, c3 = st.columns(3)
        with c1: st.markdown(f'<div class="metric-card">TEMP<br><h2>{data["current_weather"]["temperature"]}°C</h2></div>', unsafe_allow_html=True)
        with c2: st.markdown(f'<div class="metric-card">RAIN<br><h2>{rain_val}%</h2></div>', unsafe_allow_html=True)
        with c3: st.markdown(f'<div class="metric-card">WIND<br><h2>{data["current_weather"]["windspeed"]}kph</h2></div>', unsafe_allow_html=True)

        st.write("---")

        # Map logic with Light Blue theme
        st.write("### 📍 Location Pinpoint")
        map_df = pd.DataFrame({'lat': [lat], 'lon': [lon]})
        fig_map = px.scatter_mapbox(map_df, lat="lat", lon="lon", zoom=10, height=450)
        # Using "light" style for Map to get light blue water/land tones
        fig_map.update_layout(mapbox_style="carto-positron", margin={"r":0,"t":0,"l":0,"b":0})
        st.plotly_chart(fig_map, use_container_width=True)
