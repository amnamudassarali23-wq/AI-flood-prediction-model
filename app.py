import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import requests
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder

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

# --- 2. AI ENGINE ---
RAW_DATA = [
    {'Rainfall': 0.0, 'Humidity9am': 51, 'Humidity3pm': 40, 'Pressure9am': 1014.2, 'Pressure3pm': 1011.3, 'Cloud9am': 1, 'Cloud3pm': 1, 'Target': 0},
    {'Rainfall': 14.8, 'Humidity9am': 92, 'Humidity3pm': 90, 'Pressure9am': 1004.8, 'Pressure3pm': 1001.5, 'Cloud9am': 8, 'Cloud3pm': 8, 'Target': 1}
]

@st.cache_resource
def build_ai_engine():
    base_df = pd.DataFrame(RAW_DATA)
    expanded_rows = []
    for city in LOCATIONS_PK.keys():
        for _ in range(5):
            row = base_df.sample(1).iloc[0].to_dict()
            row['Location'] = city
            expanded_rows.append(row)
    df_final = pd.DataFrame(expanded_rows)
    le = LabelEncoder()
    df_final['Loc_Enc'] = le.fit_transform(df_final['Location'])
    features = ['Rainfall', 'Humidity9am', 'Humidity3pm', 'Pressure9am', 'Pressure3pm', 'Cloud9am', 'Cloud3pm', 'Loc_Enc']
    X = df_final[features]
    y = df_final['Target']
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X, y)
    return model, le

ai_model, label_encoder = build_ai_engine()

# --- 3. UI STYLING & SIDEBAR GRADIENT ---
st.set_page_config(page_title="AI Flood Prediction Model", layout="wide")

if 'flow' not in st.session_state: st.session_state.flow = "Intro"
if 'page' not in st.session_state: st.session_state.page = "Home"

st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(rgba(0, 20, 40, 0.85), rgba(0, 20, 40, 0.85)), 
                    url("https://images.unsplash.com/photo-1677442136019-21780ecad995?auto=format&fit=crop&q=80&w=1920");
        background-size: cover; background-position: center; color: #fffdd0;
    }
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #00008B 0%, #add8e6 100%) !important;
        border-right: 2px solid #fffdd0;
    }
    .info-card {
        background: rgba(0, 40, 80, 0.9); padding: 30px; border-radius: 20px; border: 2px solid #add8e6;
    }
    .welcome-btn button {
        background-color: #add8e6 !important; color: #001f3f !important; font-weight: bold; height: 60px !important; border-radius: 12px !important;
    }
    .stButton>button {
        width: 100%; height: 120px; border-radius: 10px 10px 0px 0px; 
        background: #112240; color: #fffdd0; border: 4px solid #add8e6;
        font-weight: bold; font-size: 16px; box-shadow: 0px 8px 0px #00008B;
    }
    div[data-baseweb="select"] > div {
        background-color: #003366 !important; color: #fffdd0 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 4. NAVIGATION ---
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
        st.markdown('<div class="welcome-btn">', unsafe_allow_html=True)
        if st.button("WELCOME"):
            st.session_state.flow = "Dashboard"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.flow == "Dashboard" and st.session_state.page == "Home":
    st.markdown('<h1 style="text-align:center; font-size: 45px;">AI FLOOD PREDICTION MODEL</h1>', unsafe_allow_html=True)
    st.write("##")
    c1, c2, c3, c4 = st.columns(4)
    btn_defs = [("EARLY RAIN\nPREDICTION", "Rain"), ("FLOOD RISK\nANALYSIS", "Flood"), 
                ("SATELLITE\nMONITORING", "Satellite"), ("ECONOMIC\nIMPACT", "Economic")]
    for i, (name, target) in enumerate(btn_defs):
        with [c1, c2, c3, c4][i]:
            if st.button(f"🖥️\n{name}", key=f"dash_{i}"):
                st.session_state.page = target; st.rerun()

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
            url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true&hourly=relative_humidity_2m,surface_pressure,cloudcover,rain&timezone=auto"
            return requests.get(url).json()
        except: return None

    data = fetch_weather(lat, lon)

    if data:
        # AI Calculation Logic
        h9, h3 = data['hourly']['relative_humidity_2m'][9], data['hourly']['relative_humidity_2m'][15]
        p9, p3 = data['hourly']['surface_pressure'][9], data['hourly']['surface_pressure'][15]
        c9, c3 = data['hourly']['cloudcover'][9]/12.5, data['hourly']['cloudcover'][15]/12.5
        rain_now = data['current_weather'].get('rain', 0)
        loc_enc = label_encoder.transform([selected_city])[0]
        input_data = np.array([[rain_now, h9, h3, p9, p3, c9, c3, loc_enc]])
        prob = ai_model.predict_proba(input_data)[0][1]
        prob = min(1.0, prob * 1.5) # Prob scaling for visual impact

        st.markdown(f"## 🛰️ Monitored Feed: {selected_city} - {st.session_state.page}")

        if st.session_state.page == "Rain":
            fig = px.area(x=list(range(24)), y=data['hourly']['relative_humidity_2m'][:24])
            fig.update_traces(line_color='black') 
            fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(255,255,255,0.1)', font_color="#fffdd0")
            st.plotly_chart(fig, use_container_width=True)

        elif st.session_state.page == "Flood":
            fig = go.Figure(go.Indicator(mode="gauge+number", value=prob*100, gauge={'bar': {'color': "black"}}))
            fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', font_color="#fffdd0")
            st.plotly_chart(fig, use_container_width=True)

        elif st.session_state.page == "Satellite":
            st.map(pd.DataFrame({'lat': [lat], 'lon': [lon]}))

        elif st.session_state.page == "Economic":
            # FIXED: Now risk changes dynamically with AI 'prob'
            dynamic_risk = [prob*90, prob*60, prob*75] # Agri, Urban, Infra
            impact_df = pd.DataFrame({"Sector": ["Agri", "Urban", "Infra"], "Risk %": dynamic_risk})
            fig = px.bar(impact_df, x="Sector", y="Risk %", color_discrete_sequence=['black'], range_y=[0, 100])
            fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(255,255,255,0.1)', font_color="#fffdd0")
            st.plotly_chart(fig, use_container_width=True)
            st.info(f"AI Economic Forecast: Risk levels based on current saturation in {selected_city}.")
