import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests

# --- 1. SET PAGE CONFIG ---
st.set_page_config(page_title="PAK-CLIMATE AI PRO", layout="wide", page_icon="🧪")

# --- 2. ADVANCED DARK NAVY STYLING ---
st.markdown("""
    <style>
    /* Dark Navy Gradient Background */
    .stApp {
        background: linear-gradient(135deg, #020c1b, #0a192f, #112240);
        color: #ccd6f6;
    }
    
    /* Neon Glow Title */
    .main-title {
        font-size: 45px !important;
        font-weight: 800;
        text-align: center;
        color: #64ffda;
        text-shadow: 0 0 15px rgba(100, 255, 218, 0.3);
        letter-spacing: 4px;
        padding: 20px;
    }

    /* Glassmorphic Metric Cards */
    .metric-card {
        background: rgba(17, 34, 64, 0.7);
        padding: 25px;
        border-radius: 15px;
        backdrop-filter: blur(10px);
        text-align: center;
        border: 1px solid #233554;
        transition: transform 0.3s ease;
    }
    .metric-card:hover {
        border-color: #64ffda;
        transform: translateY(-5px);
    }
    
    /* Professional Sidebar */
    [data-testid="stSidebar"] {
        background-color: #020c1b !important;
        border-right: 1px solid #233554;
    }

    /* Modern Buttons */
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        height: 70px;
        background: #112240;
        color: #64ffda;
        border: 1px solid #64ffda;
        font-weight: bold;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background: #64ffda;
        color: #020c1b;
        box-shadow: 0 0 20px rgba(100, 255, 218, 0.4);
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
        if st.button("🌧️\nRAIN\nPREDICTION"):
            st.session_state.page = "Rain"; st.rerun()
    with col2:
        if st.button("🌊\nFLOOD\nDYNAMICS"):
            st.session_state.page = "Flood"; st.rerun()
    with col3:
        if st.button("🛰️\nSATELLITE\nINTEL"):
            st.session_state.page = "Satellite"; st.rerun()
    with col4:
        if st.button("📉\nECONOMIC\nIMPACT"):
            st.session_state.page = "Economic"; st.rerun()
else:
    # --- 5. DASHBOARD VIEW ---
    with st.sidebar:
        if st.button("⬅️ RETURN TO COMMAND"):
            st.session_state.page = "Home"; st.rerun()
        st.write("---")
        selected_city = st.selectbox("🎯 SELECT OPERATIONAL AREA", sorted(list(LOCATIONS.keys())))
    
    lat, lon = LOCATIONS[selected_city]

    @st.cache_data(ttl=600)
    def fetch_weather(lat, lon):
        try:
            url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true&hourly=temperature_2m,precipitation_probability&timezone=auto"
            return requests.get(url).json()
        except:
            return None

    data = fetch_weather(lat, lon)

    if data:
        st.markdown(f'<h2 style="color:#64ffda;">📍 Operational Intel: {selected_city}</h2>', unsafe_allow_html=True)
        
        curr = data['current_weather']
        rain_val = data['hourly']['precipitation_probability'][0]
        
        # Metric Grid
        c1, c2, c3 = st.columns(3)
        with c1: st.markdown(f'<div class="metric-card"><span style="color:#8892b0">TEMP</span><h1 style="color:#64ffda">{curr["temperature"]}°C</h1></div>', unsafe_allow_html=True)
        with c2: st.markdown(f'<div class="metric-card"><span style="color:#8892b0">WIND</span><h1 style="color:#64ffda">{curr["windspeed"]}kph</h1></div>', unsafe_allow_html=True)
        with c3: st.markdown(f'<div class="metric-card"><span style="color:#8892b0">RAIN</span><h1 style="color:#64ffda">{rain_val}%</h1></div>', unsafe_allow_html=True)

        st.write("---")
        
        # Analysis Visualization
        if st.session_state.page == "Rain":
            fig = px.area(x=data['hourly']['time'][:24], y=data['hourly']['precipitation_probability'][:24], 
                          title="24h Precipitation Forecast")
            fig.update_traces(line_color='#64ffda', fillcolor='rgba(100, 255, 218, 0.2)')
            fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="#ccd6f6")
            st.plotly_chart(fig, use_container_width=True)
        
        elif st.session_state.page == "Flood":
            st.subheader("Hydrological Risk Gauge")
            fig = go.Figure(go.Indicator(
                mode = "gauge+number", value = rain_val,
                gauge = {'axis': {'range': [None, 100], 'tickcolor': "#ccd6f6"},
                         'bar': {'color': "#64ffda"},
                         'bgcolor': "#112240",
                         'steps': [{'range': [0, 70], 'color': '#233554'}, {'range': [70, 100], 'color': '#f56565'}]}))
            fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', font_color="#ccd6f6")
            st.plotly_chart(fig, use_container_width=True)

        # Map View
        st.subheader("Geospatial Target Visualization")
        st.map(pd.DataFrame({'lat': [lat], 'lon': [lon]}), zoom=11)
    else:
        st.error("📡 SATELLITE LINK LOST: Check API or Internet Connection.")
