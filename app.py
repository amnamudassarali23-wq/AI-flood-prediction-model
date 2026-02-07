import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import requests
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import LabelEncoder

# --- 1. SET PAGE CONFIG ---
st.set_page_config(page_title="AI Flood prediction model", layout="wide", page_icon="📡")

# --- 2. MACHINE LEARNING ENGINE (Merged Logic) ---
@st.cache_resource
def train_ai_model():
    try:
        # Load dataset
        df = pd.read_csv('weatherAUS.csv')
        cols = ['Date', 'Location', 'Rainfall', 'Humidity9am', 'Humidity3pm',
                'Pressure9am', 'Pressure3pm', 'Cloud9am', 'Cloud3pm', 'RainTomorrow']
        df = df[cols]
        
        # Feature Engineering: AWI
        df['Date'] = pd.to_datetime(df['Date'])
        df = df.sort_values(['Location', 'Date'])
        df['Rainfall_Clean'] = df['Rainfall'].fillna(0)
        df['AWI'] = df.groupby('Location')['Rainfall_Clean'].transform(lambda x: x.rolling(window=7, min_periods=1).sum())
        
        # Prepare Target
        df = df.dropna(subset=['RainTomorrow'])
        df['Target'] = df['RainTomorrow'].map({'No': 0, 'Yes': 1})
        
        # Encode Locations
        le = LabelEncoder()
        df['Loc_Enc'] = le.fit_transform(df['Location'])
        
        # Training
        features_list = ['Rainfall_Clean', 'Humidity9am', 'Humidity3pm', 'Pressure9am',
                         'Pressure3pm', 'Cloud9am', 'Cloud3pm', 'AWI', 'Loc_Enc']
        X = df[features_list]
        y = df['Target']
        
        imputer = SimpleImputer(strategy='median')
        X_imputed = imputer.fit_transform(X)
        
        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(X_imputed, y)
        
        return model, le, imputer
    except Exception as e:
        st.error(f"Model Training Failed: {e}")
        return None, None, None

# Initialize Model
model, le, imputer = train_ai_model()

# --- 3. UI STYLING (Navy, Cream, Blue Gradient) ---
st.markdown("""
    <style>
    .stApp { background-color: #001f3f; color: #fffdd0; }
    h1, h2, h3, p, span, label { color: #fffdd0 !important; }
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #00008B 0%, #add8e6 100%) !important;
        border-right: 2px solid #fffdd0;
    }
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

# --- 4. NAVIGATION STATE ---
if 'page' not in st.session_state:
    st.session_state.page = "Home"

LOCATIONS_PK = {
    "Islamabad": [33.6844, 73.0479], "Karachi": [24.8607, 67.0011],
    "Lahore": [31.5204, 74.3587], "Jhelum": [32.9405, 73.7276],
    "Quetta": [30.1798, 66.9750], "Gilgit": [35.9208, 74.3089]
}

# --- 5. MAIN INTERFACE ---
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
    with st.sidebar:
        st.markdown("<h3 style='color:white;'>SYSTEM CONTROL</h3>", unsafe_allow_html=True)
        if st.button("⬅️ BACK TO MENU"): st.session_state.page = "Home"; st.rerun()
        st.write("---")
        selected_city = st.selectbox("TARGET AREA", list(LOCATIONS_PK.keys()))
    
    lat, lon = LOCATIONS_PK[selected_city]
    
    # Fetch Data
    @st.cache_data(ttl=600)
    def fetch_weather(lat, lon):
        try:
            url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true&hourly=temperature_2m,relative_humidity_2m,precipitation_probability,surface_pressure,cloudcover&timezone=auto"
            return requests.get(url).json()
        except: return None

    weather_json = fetch_weather(lat, lon)

    if weather_json and model:
        # Prepare live data for prediction
        curr_h9 = weather_json['hourly']['relative_humidity_2m'][9]
        curr_h3 = weather_json['hourly']['relative_humidity_2m'][15]
        curr_p9 = weather_json['hourly']['surface_pressure'][9]
        curr_p3 = weather_json['hourly']['surface_pressure'][15]
        curr_c9 = weather_json['hourly']['cloudcover'][9] / 12.5 # Scale to 0-8
        curr_c3 = weather_json['hourly']['cloudcover'][15] / 12.5
        
        # Static AWI for demo (Calculated from rainfall in production)
        awi_val = 45.0 
        loc_enc = 0 # Default since PK cities aren't in AUS dataset
        
        # Prediction Input Array
        input_data = np.array([[0.0, curr_h9, curr_h3, curr_p9, curr_p3, curr_c9, curr_c3, awi_val, loc_enc]])
        prob = model.predict_proba(input_data)[0][1]
        
        st.markdown(f"## 🛰️ AI Monitored Feed: {selected_city}")
        
        # Metrics
        c1, c2, c3 = st.columns(3)
        with c1: st.markdown(f'<div class="metric-card">TEMP<h3>{weather_json["current_weather"]["temperature"]}°C</h3></div>', unsafe_allow_html=True)
        with c2: st.markdown(f'<div class="metric-card">AI RAIN PROB<h3>{prob*100:.1f}%</h3></div>', unsafe_allow_html=True)
        with c3: st.markdown(f'<div class="metric-card">WIND<h3>{weather_json["current_weather"]["windspeed"]}kph</h3></div>', unsafe_allow_html=True)

        st.write("---")

        if st.session_state.page == "Rain":
            fig = px.area(x=weather_json['hourly']['time'][:24], y=weather_json['hourly']['precipitation_probability'][:24],
                          color_discrete_sequence=['#add8e6'], title="Predictive Rain Intensity (24h)")
            fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="#fffdd0")
            st.plotly_chart(fig, use_container_width=True)
            st.info(f"AI Prediction: The model predicts a {prob*100:.1f}% risk of saturation tomorrow.")

        elif st.session_state.page == "Flood":
            flood_risk = (prob * 0.7) + (awi_val / 200 * 0.3)
            fig = go.Figure(go.Indicator(
                mode = "gauge+number", value = flood_risk * 100,
                title = {'text': "AI Flood Vulnerability Index"},
                gauge = {'axis': {'range': [None, 100]}, 'bar': {'color': "#add8e6"}}))
            fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', font_color="#fffdd0")
            st.plotly_chart(fig, use_container_width=True)
            
            wet_state = "Saturated" if awi_val > 100 else "Moderately Wet" if awi_val > 30 else "Dry"
            st.warning(f"Flood Monitor: Soil is {wet_state}. Combined AI Confidence: {prob:.2f}")

        elif st.session_state.page == "Satellite":
            st.map(pd.DataFrame({'lat': [lat], 'lon': [lon]}))

        elif st.session_state.page == "Economic":
            impact_df = pd.DataFrame({"Sector": ["Agriculture", "Urban Infrastructure", "Public Health"], "Risk %": [prob*80, prob*40, prob*20]})
            fig = px.bar(impact_df, x="Sector", y="Risk %", color_discrete_sequence=['#add8e6'])
            fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="#fffdd0")
            st.plotly_chart(fig, use_container_width=True)
