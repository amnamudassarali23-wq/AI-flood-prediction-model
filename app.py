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

# --- 2. EMBEDDED AI ENGINE ---
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
    X = df_final[['Rainfall', 'Humidity9am', 'Humidity3pm', 'Pressure9am', 'Pressure3pm', 'Cloud9am', 'Cloud3pm', 'Loc_Enc']]
    y = df_final['Target']
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X, y)
    return model, le

ai_model, label_encoder = build_ai_engine()

# --- 3. UI STYLING (NAVY GRADIENT SIDEBAR) ---
st.set_page_config(page_title="AI Flood Prediction", layout="wide")
st.markdown("""
    <style>
    .stApp { background-color: #001f3f; color: #fffdd0; }
    
    /* Sidebar: Mixture of Navy Blue and Light Navy Blue */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #000080 0%, #003366 100%) !important;
        border-right: 1px solid #fffdd0;
    }

    h1, h2, h3, p, span, label { color: #fffdd0 !important; }
    .stButton>button {
        width: 100%; height: 120px;
        border-radius: 10px 10px 0px 0px; 
        background: #112240; color: #fffdd0;
        border: 4px solid #003366;
        font-weight: bold; font-size: 16px;
        box-shadow: 0px 8px 0px #000080;
    }
    div[data-baseweb="select"] > div {
        background-color: #003366 !important; 
        color: #fffdd0 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 4. LOGIC ---
if 'page' not in st.session_state: st.session_state.page = "Home"

if st.session_state.page == "Home":
    st.markdown('<h1 style="text-align:center;">AI FLOOD PREDICTION MODEL</h1>', unsafe_allow_html=True)
    cols = st.columns(4)
    btn_data = [("EARLY RAIN\nPREDICTION", "Rain"), ("FLOOD RISK\nANALYSIS", "Flood"), 
                ("SATELLITE\nMONITORING", "Satellite"), ("ECONOMIC\nIMPACT", "Economic")]
    for i, (name, pg) in enumerate(btn_data):
        with cols[i]:
            if st.button(f"🖥️\n{name}"): st.session_state.page = pg; st.rerun()
else:
    with st.sidebar:
        if st.button("⬅️ BACK"): st.session_state.page = "Home"; st.rerun()
        selected_city = st.selectbox("TARGET AREA", list(LOCATIONS_PK.keys()))
    
    lat, lon = LOCATIONS_PK[selected_city]
    data = requests.get(f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true&hourly=relative_humidity_2m,surface_pressure,cloudcover,rain&timezone=auto").json()

    if data:
        st.markdown(f"## 🛰️ Monitored Feed: {selected_city}")
        
        if st.session_state.page == "Rain":
            # Graph with BLACK LINE
            fig = px.line(x=list(range(24)), y=data['hourly']['relative_humidity_2m'][:24], title="Humidity Trend")
            fig.update_traces(line_color='black') # Line color changed to Black
            fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(255,255,255,0.1)', font_color="#fffdd0")
            st.plotly_chart(fig, use_container_width=True)

        elif st.session_state.page == "Flood":
            fig = go.Figure(go.Indicator(mode="gauge+number", value=75, gauge={'bar': {'color': "black"}}))
            fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', font_color="#fffdd0")
            st.plotly_chart(fig, use_container_width=True)

        elif st.session_state.page == "Satellite":
            st.map(pd.DataFrame({'lat': [lat], 'lon': [lon]}))

        elif st.session_state.page == "Economic":
            impact = pd.DataFrame({"Sector": ["Agri", "Infra"], "Risk": [80, 50]})
            st.plotly_chart(px.bar(impact, x="Sector", y="Risk", color_discrete_sequence=['black']), use_container_width=True)
