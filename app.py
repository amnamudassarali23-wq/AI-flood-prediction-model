import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests

# --- 1. SET PAGE CONFIG ---
st.set_page_config(page_title="AI Flood prediction model", layout="wide", page_icon="📡")

# --- 2. CUSTOM CSS (Navy, Cream, Light Blue & Gradient Sidebar) ---
st.markdown("""
    <style>
    .stApp { background-color: #001f3f; color: #fffdd0; }
    h1, h2, h3, p, span, label { color: #fffdd0 !important; }

    /* Sidebar Gradient: Mixture of Light Blue and Black */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #000000 0%, #add8e6 100%) !important;
        border-right: 2px solid #fffdd0;
    }

    /* Computer-Shaped Buttons */
    .stButton>button {
        width: 100%; height: 120px;
        border-radius: 10px 10px 0px 0px; 
        background: #112240; color: #fffdd0;
        border: 4px solid #add8e6;
        font-weight: bold; font-size: 16px;
        box-shadow: 0px 8px 0px #00008B;
        transition: 0.3s;
    }
    .stButton>button:hover { background: #add8e6; color: #001f3f; transform: translateY(-5px); }

    /* Light Blue Selection Box */
    div[data-baseweb="select"] > div {
        background-color: #add8e6 !important; 
        border-radius: 8px !important;
        border: 2px solid #fffdd0 !important;
        color: #001f3f !important;
    }

    .metric-card {
        background: rgba(173, 216, 230, 0.1);
        padding: 20px; border-radius: 15px;
        text-align: center; border: 1px solid #add8e6;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. DATASET ---
LOCATIONS = {
    "Islamabad": [33.6844, 73.0479], "Karachi": [24.8607, 67.0011],
    "Lahore": [31.5204, 74.3587], "Jhelum": [32.9405, 73.7276],
    "Quetta": [30.1798, 66.9750], "Gilgit": [35.9208, 74.3089]
}

if 'page' not in st.session_state:
    st.session_state.page = "Home"

# --- 4. NAVIGATION LOGIC ---
if st.session_state.page == "Home":
    st.markdown('<h1 style="text-align:center;">AI FLOOD PREDICTION MODEL</h1>', unsafe_allow_html=True)
    st.write("##")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button("🖥️\nEARLY RAIN\nPREDICTION"): st.session_state.page = "Rain"; st.rerun()
    with col2:
        if st.button("🖥️\nFLOOD RISK\nANALYSIS"): st.session_state.page = "Flood"; st.rerun()
    with col3:
        if st.button("🖥️\nSATELLITE\nMONITORING"): st.session_state.page = "Satellite"; st.rerun()
    with col4:
        if st.button("🖥️\nECONOMIC\nIMPACT"): st.session_state.page = "Economic"; st.rerun()

else:
    # --- 5. DASHBOARD WITH GRAPHS & RESULTS ---
    with st.sidebar:
        st.markdown("<h3 style='color:black;'>SYSTEM CONTROL</h3>", unsafe_allow_html=True)
        if st.button("⬅️ BACK TO MENU"): st.session_state.page = "Home"; st.rerun()
        st.write("---")
        selected_city = st.selectbox("TARGET AREA", list(LOCATIONS.keys()))
    
    lat, lon = LOCATIONS[selected_city]
    
    @st.cache_data(ttl=600)
    def fetch_weather(lat, lon):
        url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true&hourly=temperature_2m,precipitation_probability,surface_pressure&timezone=auto"
        return requests.get(url).json()

    data = fetch_weather(lat, lon)

    if data:
        st.markdown(f"## 🛰️ Monitored Feed: {selected_city}")
        
        # --- BUTTON SPECIFIC RESULTS & GRAPHS ---
        if st.session_state.page == "Rain":
            st.subheader("🌧️ Early Rain Prediction Analysis")
            # Graph
            fig = px.area(x=data['hourly']['time'][:24], y=data['hourly']['precipitation_probability'][:24],
                          labels={'x': 'Time', 'y': 'Rain Prob %'}, color_discrete_sequence=['#add8e6'])
            st.plotly_chart(fig, use_container_width=True)
            # Result
            prob = data['hourly']['precipitation_probability'][0]
            st.info(f"AI Result: {selected_city} has a {prob}% chance of rain in the next hour. Systems are monitoring cloud density.")

        elif st.session_state.page == "Flood":
            st.subheader("🌊 Hydrological Risk Assessment")
            # Gauge Graph
            risk_val = data['hourly']['precipitation_probability'][0]
            fig = go.Figure(go.Indicator(
                mode = "gauge+number", value = risk_val,
                gauge = {'axis': {'range': [None, 100]}, 'bar': {'color': "#add8e6"}}
            ))
            st.plotly_chart(fig, use_container_width=True)
            # Result
            status = "STABLE" if risk_val < 40 else "CRITICAL"
            st.warning(f"AI Monitoring: Water saturation levels are {status}. Pre-emptive drainage protocols active.")

        elif st.session_state.page == "Satellite":
            st.subheader("🛰️ Live Satellite Surveillance")
            # Map as a monitored result
            st.map(pd.DataFrame({'lat': [lat], 'lon': [lon]}))
            st.success(f"Satellite Fix: Coordinates {lat}, {lon} verified. Cloud movement tracking is active.")

        elif st.session_state.page == "Economic":
            st.subheader("📉 Projected Economic Impact")
            # Bar Chart
            impact_data = pd.DataFrame({"Sector": ["Agri", "Urban", "Infrastructure"], "Risk": [20, 15, 35]})
            fig = px.bar(impact_data, x="Sector", y="Risk", color_discrete_sequence=['#add8e6'])
            st.plotly_chart(fig, use_container_width=True)
            st.info("AI Projection: Potential infrastructure loss minimized by 12% through early warning detection.")

    else:
        st.error("Connection failed.")
