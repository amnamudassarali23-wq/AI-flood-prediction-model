import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests

# --- 1. SET PAGE CONFIG (Updated Title) ---
st.set_page_config(page_title="AI Flood prediction model", layout="wide", page_icon="📡")

# --- 2. THE BLUE-ONLY CSS (Strictly No Green, No Pink) ---
st.markdown("""
    <style>
    /* Dark Navy & Deep Steel Background */
    .stApp {
        background: linear-gradient(160deg, #020c1b 0%, #0a192f 50%, #0d2538 100%);
        color: #ccd6f6;
    }
    
    /* Neon Cyan Title */
    .main-title {
        font-size: 48px !important;
        font-weight: 900;
        text-align: center;
        color: #64ffda;
        text-shadow: 0 0 20px rgba(100, 255, 218, 0.4);
        letter-spacing: 5px;
        padding-top: 30px;
    }

    /* Navy Glass Cards */
    .metric-card {
        background: rgba(16, 33, 65, 0.8);
        padding: 30px;
        border-radius: 12px;
        backdrop-filter: blur(12px);
        text-align: center;
        border: 2px solid #1e3a8a;
        transition: 0.3s;
    }
    .metric-card:hover {
        border-color: #64ffda;
        background: rgba(20, 45, 90, 0.9);
    }
    
    /* Sidebar Navigation */
    [data-testid="stSidebar"] {
        background-color: #020c1b !important;
        border-right: 2px solid #1e3a8a;
    }

    /* Tactical Blue Buttons */
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        height: 65px;
        background: #112240;
        color: #64ffda;
        border: 1px solid #1e3a8a;
        font-weight: 800;
        letter-spacing: 1px;
    }
    .stButton>button:hover {
        background: #1e3a8a;
        color: white;
        border-color: #64ffda;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. LOCATIONS ---
LOCATIONS = {
    "Islamabad": [33.6844, 73.0479], "Karachi": [24.8607, 67.0011],
    "Lahore": [31.5204, 74.3587], "Jhelum": [32.9405, 73.7276],
    "Rawalpindi": [33.5651, 73.0169], "Faisalabad": [31.4504, 73.1350],
    "Quetta": [30.1798, 66.9750], "Gilgit": [35.9208, 74.3089]
}

if 'page' not in st.session_state:
    st.session_state.page = "Home"

# --- 4. NAVIGATION LOGIC ---
if st.session_state.page == "Home":
    st.markdown('<p class="main-title">AI FLOOD PREDICTION MODEL</p>', unsafe_allow_html=True)
    st.write("##")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button("🌧️ PRECIPITATION"):
            st.session_state.page = "Rain"; st.rerun()
    with col2:
        if st.button("🌊 HYDRO-RISK"):
            st.session_state.page = "Flood"; st.rerun()
    with col3:
        if st.button("🛰️ SURVEILLANCE"):
            st.session_state.page = "Satellite"; st.rerun()
    with col4:
        if st.button("📉 ANALYTICS"):
            st.session_state.page = "Economic"; st.rerun()
else:
    # --- 5. OPERATIONAL INTERFACE ---
    with st.sidebar:
        st.markdown("<h2 style='color:#64ffda;'>SYSTEM CONTROL</h2>", unsafe_allow_html=True)
        if st.button("⬅️ EXIT TO MAIN"):
            st.session_state.page = "Home"; st.rerun()
        st.write("---")
        selected_city = st.selectbox("TARGET ZONE", sorted(list(LOCATIONS.keys())))
    
    lat, lon = LOCATIONS[selected_city]

    @st.cache_data(ttl=600)
    def fetch_weather(lat, lon):
        try:
            url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true&hourly=temperature_2m,precipitation_probability,surface_pressure&timezone=auto"
            return requests.get(url).json()
        except: return None

    data = fetch_weather(lat, lon)

    if data:
        st.markdown(f'<h2 style="color:#64ffda; letter-spacing:2px;">ZONE: {selected_city.upper()}</h2>', unsafe_allow_html=True)
        
        curr = data['current_weather']
        rain_val = data['hourly']['precipitation_probability'][0]
        pressure = data['hourly']['surface_pressure'][0]
        
        c1, c2, c3, c4 = st.columns(4)
        with c1: st.markdown(f'<div class="metric-card"><span style="color:#8892b0">TEMP</span><h2 style="color:#64ffda">{curr["temperature"]}°C</h2></div>', unsafe_allow_html=True)
        with c2: st.markdown(f'<div class="metric-card"><span style="color:#8892b0">WIND</span><h2 style="color:#64ffda">{curr["windspeed"]}km/h</h2></div>', unsafe_allow_html=True)
        with c3: st.markdown(f'<div class="metric-card"><span style="color:#8892b0">RAIN</span><h2 style="color:#64ffda">{rain_val}%</h2></div>', unsafe_allow_html=True)
        with c4: st.markdown(f'<div class="metric-card"><span style="color:#8892b0">BARO</span><h2 style="color:#64ffda">{int(pressure)}hPa</h2></div>', unsafe_allow_html=True)

        st.write("---")
        
        if st.session_state.page == "Rain":
            fig = px.line(x=data['hourly']['time'][:24], y=data['hourly']['precipitation_probability'][:24], 
                          title="Operational Rain Forecast (24H)")
            fig.update_traces(line_color='#64ffda', line_width=4)
            fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="#ccd6f6")
            st.plotly_chart(fig, use_container_width=True)
        
        elif st.session_state.page == "Flood":
            st.subheader("Hydrological Risk Assessment")
            fig = go.Figure(go.Indicator(
                mode = "gauge+number", value = rain_val,
                gauge = {'axis': {'range': [None, 100], 'tickcolor': "#ccd6f6"},
                         'bar': {'color': "#64ffda"},
                         'bgcolor': "#020c1b",
                         'steps': [{'range': [0, 50], 'color': '#112240'}, {'range': [50, 100], 'color': '#1e3a8a'}]}))
            fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', font_color="#ccd6f6")
            st.plotly_chart(fig, use_container_width=True)

        # Map View (Dark)
        st.subheader("📍 Geospatial Fix")
        map_df = pd.DataFrame({'lat': [lat], 'lon': [lon]})
        fig_map = px.scatter_mapbox(map_df, lat="lat", lon="lon", zoom=10, height=400)
        fig_map.update_layout(mapbox_style="carto-darkmatter", margin={"r":0,"t":0,"l":0,"b":0})
        st.plotly_chart(fig_map, use_container_width=True)

    else:
        st.error("COMMUNICATION ERROR: LINK TO METEO-SAT BROKEN.")
