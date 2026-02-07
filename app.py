import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import requests

# --- 1. COORDINATES FOR 37 PAKISTANI CITIES ---
LOCATIONS_PK = {
    "Karachi": [24.86, 67.00], "Lahore": [31.52, 74.35], "Faisalabad": [31.45, 73.13], 
    "Rawalpindi": [33.60, 73.04], "Gujranwala": [32.18, 74.19], "Peshawar": [34.01, 71.52], 
    "Multan": [30.15, 71.45], "Hyderabad": [25.39, 68.37], "Islamabad": [33.68, 73.04], 
    "Quetta": [30.17, 66.97], "Sargodha": [32.08, 72.67], "Sialkot": [32.49, 74.52], 
    "Bahawalpur": [29.35, 71.69], "Sukkur": [27.72, 68.82], "Jhang": [31.27, 72.33], 
    "Sheikhupura": [31.71, 73.98], "Rahim Yar Khan": [28.42, 70.29], "Dera Ghazi Khan": [30.04, 70.63], 
    "Gujrat": [32.57, 74.07], "Sahiwal": [30.66, 73.11], "Wah": [33.77, 72.75], 
    "Mardan": [34.19, 72.04], "Kasur": [31.11, 74.45], "Okara": [30.81, 73.45], 
    "Mingora": [34.77, 72.36], "Nawabshah": [26.24, 68.41], "Chiniot": [31.72, 72.97], 
    "Kotri": [25.37, 68.31], "Kamoke": [32.01, 74.22], "Hafizabad": [32.06, 73.68], 
    "Sadiqabad": [28.31, 70.13], "Mirpur Khas": [25.52, 69.01], "Burewala": [30.15, 72.68], 
    "Kohat": [33.58, 71.44], "Khanewal": [30.30, 71.93], "Dera Ismail Khan": [31.83, 70.90], 
    "Muzaffargarh": [30.07, 71.19]
}

# --- 2. SET PAGE CONFIG & SESSION STATE ---
st.set_page_config(page_title="AI Flood Prediction Model", layout="wide", page_icon="📡")

if 'flow' not in st.session_state: st.session_state.flow = "Intro"
if 'page' not in st.session_state: st.session_state.page = "Home"

# --- 3. CUSTOM CSS ---
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(rgba(0, 20, 40, 0.85), rgba(0, 20, 40, 0.85)), 
                    url("https://images.unsplash.com/photo-1677442136019-21780ecad995?auto=format&fit=crop&q=80&w=1920");
        background-size: cover; background-position: center; color: #fffdd0;
    }
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #000080 0%, #003366 100%) !important;
        border-right: 2px solid #fffdd0;
    }
    .info-card {
        background: rgba(0, 40, 80, 0.9); padding: 30px; border-radius: 20px;
        border: 2px solid #add8e6; box-shadow: 0px 10px 30px rgba(0,0,0,0.5);
    }
    .welcome-btn button {
        background-color: #add8e6 !important; color: #001f3f !important;
        height: 60px !important; font-size: 20px !important; border-radius: 12px !important;
    }
    .stButton>button {
        width: 100%; height: 120px; border-radius: 10px 10px 0px 0px; 
        background: #112240; color: #fffdd0; border: 4px solid #add8e6;
        font-weight: bold; font-size: 16px; box-shadow: 0px 8px 0px #00008B;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 4. NAVIGATION LOGIC ---

# PAGE 1: INTRO (AI Neurons + Info Box)
if st.session_state.flow == "Intro":
    st.write("##")
    st.markdown('<h1 style="text-align:center; font-size: 55px; text-shadow: 2px 2px 10px #000;">AI FLOOD PREDICTION MODEL</h1>', unsafe_allow_html=True)
    st.write("##")
    
    col_left, col_right = st.columns([2.5, 1])
    with col_left:
        st.markdown(f"""
        <div class="info-card">
            <h2 style="color:#add8e6;">International Islamic University Islamabad</h2>
            <p style="font-size: 19px;"><b>Department:</b> BE.tech AI (Electrical and Computer Engineering)</p>
            <p style="font-size: 19px;"><b>Professor:</b> Engr. Asad</p>
            <hr style="opacity: 0.2;">
            <p style="font-size: 17px;"><b>Team:</b> Amna Mudassar Ali, Fatima Arshad, Ayesha Bint e Israr, Tehreen Ramesha</p>
            <p style="font-size: 17px;"><b>Roll No:</b> 016809, 012221, 012214, 012218</p>
        </div>
        """, unsafe_allow_html=True)
    with col_right:
        st.write("##")
        st.write("##")
        st.markdown('<div class="welcome-btn">', unsafe_allow_html=True)
        if st.button("WELCOME"):
            st.session_state.flow = "Dashboard"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# PAGE 2: DASHBOARD
elif st.session_state.flow == "Dashboard" and st.session_state.page == "Home":
    st.markdown('<h1 style="text-align:center;">AI FLOOD PREDICTION MODEL</h1>', unsafe_allow_html=True)
    st.write("##")
    c1, c2, c3, c4 = st.columns(4)
    with c1: 
        if st.button("🖥️\nEARLY RAIN\nPREDICTION"): st.session_state.page = "Rain"; st.rerun()
    with c2: 
        if st.button("🖥️\nFLOOD RISK\nANALYSIS"): st.session_state.page = "Flood"; st.rerun()
    with c3: 
        if st.button("🖥️\nSATELLITE\nMONITORING"): st.session_state.page = "Satellite"; st.rerun()
    with c4: 
        if st.button("🖥️\nECONOMIC\nIMPACT"): st.session_state.page = "Economic"; st.rerun()

# PAGE 3: FEATURE PAGES (With Live API Data)
else:
    with st.sidebar:
        st.markdown("<h3 style='color:white;'>SYSTEM CONTROL</h3>", unsafe_allow_html=True)
        if st.button("⬅️ DASHBOARD"): st.session_state.page = "Home"; st.rerun()
        if st.button("🏠 MAIN PAGE"): st.session_state.flow = "Intro"; st.session_state.page = "Home"; st.rerun()
        st.write("---")
        selected_city = st.selectbox("TARGET AREA", list(LOCATIONS_PK.keys()))
    
    lat, lon = LOCATIONS_PK[selected_city]
    
    @st.cache_data(ttl=600)
    def fetch_weather(lat, lon):
        try:
            url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true&hourly=temperature_2m,precipitation_probability,surface_pressure&timezone=auto"
            return requests.get(url).json()
        except: return None

    data = fetch_weather(lat, lon)

    if data:
        st.markdown(f"## 🛰️ Monitored Feed: {selected_city} - {st.session_state.page}")
        
        if st.session_state.page == "Rain":
            fig = px.area(x=data['hourly']['time'][:24], y=data['hourly']['precipitation_probability'][:24])
            fig.update_traces(line_color='black') 
            fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="#fffdd0")
            st.plotly_chart(fig, use_container_width=True)
            st.info(f"AI Prediction: Chance of Rain is {data['hourly']['precipitation_probability'][0]}%.")

        elif st.session_state.page == "Flood":
            risk = data['hourly']['precipitation_probability'][0]
            fig = go.Figure(go.Indicator(mode="gauge+number", value=risk, gauge={'bar': {'color': "black"}}))
            fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', font_color="#fffdd0")
            st.plotly_chart(fig, use_container_width=True)

        elif st.session_state.page == "Satellite":
            st.map(pd.DataFrame({'lat': [lat], 'lon': [lon]}))

        elif st.session_state.page == "Economic":
            impact_df = pd.DataFrame({"Sector": ["Agri", "Urban", "Infra"], "Risk": [25, 15, 30]})
            fig = px.bar(impact_df, x="Sector", y="Risk", color_discrete_sequence=['black'])
            fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="#fffdd0")
            st.plotly_chart(fig, use_container_width=True)
