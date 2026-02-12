import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import requests
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder

# Comprehensive Dictionary of major cities & all district headquarters across Pakistan
LOCATIONS_PK = {
    # PUNJAB (Major & Districts)
    "Lahore": [31.55, 74.34], "Faisalabad": [31.42, 73.08], "Rawalpindi": [33.60, 73.03],
    "Gujranwala": [32.16, 74.19], "Multan": [30.20, 71.47], "Sialkot": [32.50, 74.53],
    "Bahawalpur": [29.35, 71.69], "Sargodha": [32.08, 72.67], "Sahiwal": [30.66, 73.11],
    "Gujrat": [32.57, 74.07], "Sheikhupura": [31.71, 73.98], "Jhang": [31.27, 72.33],
    "Rahim Yar Khan": [28.42, 70.29], "Kasur": [31.11, 74.45], "Okara": [30.81, 73.45],
    "Dera Ghazi Khan": [30.04, 70.63], "Chiniot": [31.72, 72.97], "Hafizabad": [32.06, 73.68],
    "Mandi Bahauddin": [32.58, 73.48], "Attock": [33.76, 72.36], "Chakwal": [32.93, 72.85],
    "Jhelum": [32.94, 73.72], "Khushab": [32.29, 72.35], "Mianwali": [32.58, 71.51],
    "Bhakkar": [31.62, 71.06], "Layyah": [30.96, 70.94], "Muzaffargarh": [30.07, 71.19],
    "Rajanpur": [29.10, 70.32], "Lodhran": [29.54, 71.63], "Vehari": [30.04, 72.35],
    "Khanewal": [30.30, 71.93], "Pakpattan": [30.34, 73.38], "Bahawalnagar": [29.99, 73.25],
    "Nankana Sahib": [31.44, 73.70], "Murree": [33.90, 73.39], "Wah Cantt": [33.77, 72.75],
    
    # SINDH (Major & Districts)
    "Karachi": [24.86, 67.01], "Hyderabad": [25.38, 68.37], "Sukkur": [27.72, 68.82],
    "Larkana": [27.55, 68.20], "Nawabshah": [26.24, 68.41], "Mirpur Khas": [25.52, 69.01],
    "Jacobabad": [28.28, 68.43], "Shikarpur": [27.95, 68.63], "Thatta": [24.74, 67.92],
    "Dadu": [26.73, 67.77], "Badin": [24.65, 68.83], "Ghotki": [28.00, 69.31],
    "Khairpur": [27.52, 68.75], "Umarkot": [25.36, 69.73], "Sanghar": [26.04, 68.94],
    "Tharparkar": [24.87, 70.10], "Kashmore": [28.43, 69.33], "Jamshoro": [25.43, 68.26],
    "Tando Allahyar": [25.46, 68.71], "Tando Muhammad Khan": [25.12, 68.53], "Matiari": [25.59, 68.44],
    
    # KHYBER PAKHTUNKHWA (Major & Districts)
    "Peshawar": [34.01, 71.56], "Mardan": [34.19, 72.04], "Mingora": [34.77, 72.36],
    "Abbottabad": [34.16, 73.22], "Kohat": [33.58, 71.44], "Dera Ismail Khan": [31.83, 70.90],
    "Nowshera": [34.01, 71.97], "Swabi": [34.12, 72.46], "Charsadda": [34.14, 71.73],
    "Mansehra": [34.33, 73.19], "Haripur": [33.99, 72.93], "Bannu": [32.98, 70.60],
    "Karak": [33.11, 71.09], "Lakki Marwat": [32.60, 70.91], "Tank": [32.22, 70.37],
    "Chitral": [35.85, 71.78], "Dir": [35.20, 71.87], "Malakand": [34.56, 71.92],
    "Swat": [34.80, 72.35], "Shangla": [34.88, 72.75], "Battagram": [34.67, 73.02],
    "Kohistan": [35.25, 73.31], "Bajaur": [34.78, 71.52], "Khyber": [33.91, 71.08],
    "Kurram": [33.82, 70.11], "Mohmand": [34.42, 71.45], "Waziristan": [32.30, 69.85],
    
    # BALOCHISTAN (Major & Districts)
    "Quetta": [30.18, 67.00], "Gwadar": [25.12, 62.32], "Turbat": [26.00, 63.04],
    "Khuzdar": [27.81, 66.61], "Chaman": [30.91, 66.45], "Sibi": [29.54, 67.87],
    "Loralai": [30.37, 68.59], "Zhob": [31.34, 69.45], "Kalat": [29.02, 66.59],
    "Nushki": [29.55, 66.02], "Panjgur": [26.96, 64.09], "Kharan": [28.58, 65.41],
    "Mastung": [29.79, 66.84], "Ziarat": [30.38, 67.72], "Pishin": [30.58, 66.99],
    "Dera Bugti": [29.03, 69.15], "Kohlu": [29.89, 69.25], "Barkhan": [29.89, 69.72],
    "Musakhel": [30.86, 69.81], "Jafarabad": [28.35, 68.21], "Nasirabad": [28.51, 68.22],
    "Lasbela": [25.84, 66.32], "Awaran": [25.98, 65.22], "Washuk": [27.53, 64.71],
    
    # GILGIT-BALTISTAN, AJK & ISLAMABAD
    "Islamabad": [33.69, 73.06], "Muzaffarabad": [34.37, 73.47], "Mirpur": [33.14, 73.75],
    "Kotli": [33.51, 73.90], "Bagh": [33.98, 73.77], "Rawalakot": [33.85, 73.76],
    "Gilgit": [35.92, 74.30], "Skardu": [35.29, 75.63], "Hunza": [36.31, 74.64],
    "Diamer": [35.41, 74.10], "Astore": [35.36, 74.85], "Ghanche": [35.19, 76.33]
}

@st.cache_resource
def build_ai_engine():
    # Training Data Simulation (Updated for more robust features)
    raw_data = [
        {'Rainfall': 0.0, 'Humidity9am': 51, 'Humidity3pm': 40, 'Pressure9am': 1014.2, 'Pressure3pm': 1011.3, 'Cloud9am': 1, 'Cloud3pm': 1, 'Target': 0},
        {'Rainfall': 14.8, 'Humidity9am': 92, 'Humidity3pm': 90, 'Pressure9am': 1004.8, 'Pressure3pm': 1001.5, 'Cloud9am': 8, 'Cloud3pm': 8, 'Target': 1},
        {'Rainfall': 2.1, 'Humidity9am': 70, 'Humidity3pm': 65, 'Pressure9am': 1010.1, 'Pressure3pm': 1008.2, 'Cloud9am': 4, 'Cloud3pm': 5, 'Target': 0}
    ]
    base_df = pd.DataFrame(raw_data)
    expanded_rows = []
    for city in LOCATIONS_PK.keys():
        for _ in range(10):  # Increased sample size for better city-specific encoding
            row = base_df.sample(1).iloc[0].to_dict()
            row['Location'] = city
            expanded_rows.append(row)
    df_final = pd.DataFrame(expanded_rows)
    le = LabelEncoder()
    df_final['Loc_Enc'] = le.fit_transform(df_final['Location'])
    features = ['Rainfall', 'Humidity9am', 'Humidity3pm', 'Pressure9am', 'Pressure3pm', 'Cloud9am', 'Cloud3pm', 'Loc_Enc']
    X, y = df_final[features], df_final['Target']
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X, y)
    return model, le

ai_model, label_encoder = build_ai_engine()

st.set_page_config(page_title="AI National Flood Prediction", layout="wide")

if 'flow' not in st.session_state: st.session_state.flow = "Intro"
if 'page' not in st.session_state: st.session_state.page = "Home"

# Futuristic UI styling
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(rgba(0, 20, 40, 0.9), rgba(0, 20, 40, 0.9)), 
                    url("https://images.unsplash.com/photo-1545042157-0103730761e0?auto=format&fit=crop&q=80&w=1920");
        background-size: cover; color: #fffdd0;
    }
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #000033 0%, #004080 100%) !important;
        border-right: 2px solid #add8e6;
    }
    .info-card {
        background: rgba(0, 40, 80, 0.9); padding: 30px; border-radius: 20px; border: 2px solid #add8e6;
    }
    .stButton>button {
        width: 100%; height: 100px; background: #112240; color: #fffdd0; border: 2px solid #add8e6;
        font-weight: bold; transition: 0.3s;
    }
    .stButton>button:hover { background: #add8e6; color: #001f3f; }
    </style>
    """, unsafe_allow_html=True)

if st.session_state.flow == "Intro":
    st.write("##")
    st.markdown('<h1 style="text-align:center; font-size: 55px; color:#add8e6;">NATIONAL AI FLOOD MONITOR</h1>', unsafe_allow_html=True)
    st.write("##")
    col_left, col_right = st.columns([2.5, 1])
    with col_left:
        st.markdown(f"""
        <div class="info-card">
            <h2 style="color:#add8e6;">International Islamic University Islamabad</h2>
            <p><b>Program:</b> B.E Tech(AI) | <b>Supervisor:</b> Engr. Asad</p>
            <p><b>National Scale Analysis:</b> Monitoring {len(LOCATIONS_PK)} Strategic Areas</p>
            <hr style="opacity: 0.2;">
            <p style="font-size: 14px;"><b>Team:</b> Amna Mudassar Ali, Fatima Arshad, Ayesha Bint e Israr, Tehreen Ramesha</p>
        </div>
        """, unsafe_allow_html=True)
    with col_right:
        st.write("##")
        if st.button("LAUNCH DASHBOARD"):
            st.session_state.flow = "Dashboard"
            st.rerun()

elif st.session_state.flow == "Dashboard" and st.session_state.page == "Home":
    st.markdown('<h1 style="text-align:center;">PAKISTAN STRATEGIC AI DASHBOARD</h1>', unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    pages = [("PRECIPITATION", "Rain"), ("RISK ANALYTICS", "Flood"), ("LIVE MAP", "Satellite"), ("ECONOMY", "Economic")]
    for i, (name, target) in enumerate(pages):
        with [c1, c2, c3, c4][i]:
            if st.button(f"📊\n{name}"):
                st.session_state.page = target; st.rerun()

else:
    with st.sidebar:
        st.markdown("<h3 style='color:white;'>SYSTEM CONTROL</h3>", unsafe_allow_html=True)
        if st.button("⬅️ DASHBOARD"): st.session_state.page = "Home"; st.rerun()
        if st.button("🏠 MAIN PAGE"): st.session_state.flow = "Intro"; st.session_state.page = "Home"; st.rerun()
        st.write("---")
        # Alphabetical search for easy access
        selected_city = st.selectbox("SELECT REGION", sorted(list(LOCATIONS_PK.keys())))
    
    lat, lon = LOCATIONS_PK[selected_city]
    
    @st.cache_data(ttl=600)
    def fetch_weather(lat, lon):
        try:
            url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true&hourly=relative_humidity_2m,surface_pressure,cloudcover,rain&timezone=auto"
            return requests.get(url).json()
        except: return None

    data = fetch_weather(lat, lon)

    if data:
        # Pre-processing live data for the AI model
        h9, h3 = data['hourly']['relative_humidity_2m'][9], data['hourly']['relative_humidity_2m'][15]
        p9, p3 = data['hourly']['surface_pressure'][9], data['hourly']['surface_pressure'][15]
        c9, c3 = data['hourly']['cloudcover'][9]/12.5, data['hourly']['cloudcover'][15]/12.5
        rain_now = data['current_weather'].get('rain', 0)
        loc_enc = label_encoder.transform([selected_city])[0]
        
        input_data = np.array([[rain_now, h9, h3, p9, p3, c9, c3, loc_enc]])
        prob = ai_model.predict_proba(input_data)[0][1]
        prob = min(1.0, prob * 1.5) 

        st.markdown(f"## 🛰️ {selected_city} Intelligence Feed")

        if st.session_state.page == "Rain":
            fig = px.area(x=list(range(24)), y=data['hourly']['relative_humidity_2m'][:24], title="24h Relative Humidity Trend")
            fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(255,255,255,0.1)', font_color="#fffdd0")
            st.plotly_chart(fig, use_container_width=True)

        elif st.session_state.page == "Flood":
            fig = go.Figure(go.Indicator(mode="gauge+number", value=prob*100, title={'text': "AI Flood Probability %"},
                                       gauge={'bar': {'color': "#add8e6"}, 'axis': {'range': [0, 100]}}))
            fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', font_color="#fffdd0")
            st.plotly_chart(fig, use_container_width=True)

        elif st.session_state.page == "Satellite":
            st.map(pd.DataFrame({'lat': [lat], 'lon': [lon]}))

        elif st.session_state.page == "Economic":
            impact_df = pd.DataFrame({"Sector": ["Agriculture", "Urban Infrastructure", "Power Grid"], 
                                     "Risk %": [prob*95, prob*65, prob*78]})
            fig = px.bar(impact_df, x="Sector", y="Risk %", color="Sector", range_y=[0, 100], color_discrete_sequence=['#add8e6', '#004080', '#000033'])
            fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(255,255,255,0.1)', font_color="#fffdd0")
            st.plotly_chart(fig, use_container_width=True)
