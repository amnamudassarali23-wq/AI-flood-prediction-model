import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import requests
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder

# Comprehensive District-Level Dictionary for All Pakistan
LOCATIONS_PK = {
    # PUNJAB
    "Lahore": [31.52, 74.35], "Faisalabad": [31.45, 73.13], "Rawalpindi": [33.60, 73.04], 
    "Gujranwala": [32.18, 74.19], "Multan": [30.15, 71.45], "Sialkot": [32.49, 74.52], 
    "Bahawalpur": [29.35, 71.69], "Sargodha": [32.08, 72.67], "Sahiwal": [30.66, 73.11], 
    "Gujrat": [32.57, 74.07], "Sheikhupura": [31.71, 73.98], "Jhang": [31.27, 72.33], 
    "Rahim Yar Khan": [28.42, 70.29], "Kasur": [31.11, 74.45], "Okara": [30.81, 73.45], 
    "Dera Ghazi Khan": [30.04, 70.63], "Chiniot": [31.72, 72.97], "Hafizabad": [32.06, 73.68], 
    "Mandi Bahauddin": [32.58, 73.48], "Attock": [33.76, 72.36], "Chakwal": [32.93, 72.85], 
    "Jhelum": [32.94, 73.72], "Khushab": [32.29, 72.35], "Mianwali": [32.58, 71.51], 
    "Bhakkar": [31.62, 71.06], "Layyah": [30.96, 70.94], "Muzaffargarh": [30.07, 71.19], 
    "Rajanpur": [29.10, 70.32], "Lodhran": [29.54, 71.63], "Vehari": [30.04, 72.35], 
    "Khanewal": [30.30, 71.93], "Pakpattan": [30.34, 73.38], "Bahawalnagar": [29.99, 73.25], 
    "Nankana Sahib": [31.44, 73.70], "Narowal": [32.10, 74.87], "Toba Tek Singh": [31.13, 72.48],
    # SINDH
    "Karachi": [24.86, 67.00], "Hyderabad": [25.39, 68.37], "Sukkur": [27.72, 68.82], 
    "Larkana": [27.55, 68.20], "Nawabshah": [26.24, 68.41], "Mirpur Khas": [25.52, 69.01], 
    "Jacobabad": [28.28, 68.43], "Shikarpur": [27.95, 68.63], "Thatta": [24.74, 67.92], 
    "Dadu": [26.73, 67.77], "Badin": [24.65, 68.83], "Ghotki": [28.00, 69.31], 
    "Khairpur": [27.52, 68.75], "Umarkot": [25.36, 69.73], "Sanghar": [26.04, 68.94], 
    "Tharparkar": [24.87, 70.10], "Kashmore": [28.43, 69.33], "Jamshoro": [25.43, 68.26], 
    "Tando Allahyar": [25.46, 68.71], "Tando Muhammad Khan": [25.12, 68.53], "Matiari": [25.59, 68.44], 
    "Kambar Shahdadkot": [27.58, 67.98], "Sujawal": [24.60, 68.07], "Malir": [24.90, 67.19],
    # KHYBER PAKHTUNKHWA
    "Peshawar": [34.01, 71.52], "Mardan": [34.19, 72.04], "Mingora": [34.77, 72.36], 
    "Abbottabad": [34.16, 73.22], "Kohat": [33.58, 71.44], "Dera Ismail Khan": [31.83, 70.90], 
    "Nowshera": [34.01, 71.97], "Swabi": [34.12, 72.46], "Charsadda": [34.14, 71.73], 
    "Mansehra": [34.33, 73.19], "Haripur": [33.99, 72.93], "Bannu": [32.98, 70.60], 
    "Karak": [33.11, 71.09], "Lakki Marwat": [32.60, 70.91], "Tank": [32.22, 70.37], 
    "Chitral": [35.85, 71.78], "Upper Dir": [35.20, 71.87], "Lower Dir": [34.84, 71.84], 
    "Malakand": [34.56, 71.92], "Swat": [34.80, 72.35], "Shangla": [34.88, 72.75], 
    "Battagram": [34.67, 73.02], "Upper Kohistan": [35.25, 73.31], "Lower Kohistan": [35.15, 73.21], 
    "Bajaur": [34.78, 71.52], "Khyber": [33.91, 71.08], "Kurram": [33.82, 70.11], 
    "Mohmand": [34.42, 71.45], "North Waziristan": [32.97, 70.06], "South Waziristan": [32.30, 69.85], 
    "Hangu": [33.53, 71.05], "Buner": [34.39, 72.61], "Torghar": [34.52, 72.84],
    # BALOCHISTAN
    "Quetta": [30.17, 66.97], "Gwadar": [25.12, 62.32], "Turbat": [26.00, 63.04], 
    "Khuzdar": [27.81, 66.61], "Chaman": [30.91, 66.45], "Sibi": [29.54, 67.87], 
    "Loralai": [30.37, 68.59], "Zhob": [31.34, 69.45], "Kalat": [29.02, 66.59], 
    "Nushki": [29.55, 66.02], "Panjgur": [26.96, 64.09], "Kharan": [28.58, 65.41], 
    "Mastung": [29.79, 66.84], "Ziarat": [30.38, 67.72], "Pishin": [30.58, 66.99], 
    "Dera Bugti": [29.03, 69.15], "Kohlu": [29.89, 69.25], "Barkhan": [29.89, 69.72], 
    "Musakhel": [30.86, 69.81], "Jafarabad": [28.35, 68.21], "Nasirabad": [28.51, 68.22], 
    "Lasbela": [25.84, 66.32], "Awaran": [25.98, 65.22], "Washuk": [27.53, 64.71], 
    "Chagai": [29.05, 64.41], "Duki": [30.15, 68.57], "Harnai": [30.10, 67.93], 
    "Jhal Magsi": [28.37, 67.62], "Kachhi": [29.03, 67.60], "Killa Abdullah": [30.73, 66.60], 
    "Killa Saifullah": [30.70, 68.23], "Sohbatpur": [28.52, 68.54], "Surab": [28.49, 66.26],
    # AJK, GB & ISLAMABAD
    "Islamabad": [33.68, 73.04], "Muzaffarabad": [34.37, 73.47], "Mirpur": [33.14, 73.75], 
    "Kotli": [33.51, 73.90], "Bagh": [33.98, 73.77], "Rawalakot": [33.85, 73.76], 
    "Bhimber": [32.97, 73.91], "Neelum": [34.59, 73.91], "Haveli": [33.92, 74.10], 
    "Sudhnoti": [33.71, 73.68], "Gilgit": [35.92, 74.30], "Skardu": [35.29, 75.63], 
    "Hunza": [36.31, 74.64], "Diamer": [35.41, 74.10], "Astore": [35.36, 74.85], 
    "Ghanche": [35.19, 76.33], "Ghizer": [36.17, 73.58], "Kharmang": [34.93, 76.12], 
    "Shigar": [35.42, 75.73], "Nagar": [36.21, 74.70]
}

@st.cache_resource
def build_ai_engine():
    raw_data = [
        {'Rainfall': 0.0, 'Humidity9am': 51, 'Humidity3pm': 40, 'Pressure9am': 1014.2, 'Pressure3pm': 1011.3, 'Cloud9am': 1, 'Cloud3pm': 1, 'Target': 0},
        {'Rainfall': 14.8, 'Humidity9am': 92, 'Humidity3pm': 90, 'Pressure9am': 1004.8, 'Pressure3pm': 1001.5, 'Cloud9am': 8, 'Cloud3pm': 8, 'Target': 1}
    ]
    base_df = pd.DataFrame(raw_data)
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
    X, y = df_final[features], df_final['Target']
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X, y)
    return model, le

ai_model, label_encoder = build_ai_engine()

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

if st.session_state.flow == "Intro":
    st.write("##")
    st.markdown('<h1 style="text-align:center; font-size: 55px; text-shadow: 2px 2px 10px #000;">AI FLOOD PREDICTION MODEL</h1>', unsafe_allow_html=True)
    st.write("##")
    col_left, col_right = st.columns([2.5, 1])
    with col_left:
        st.markdown(f"""
        <div class="info-card">
            <h2 style="color:#add8e6;">International Islamic University Islamabad</h2>
            <p style="font-size: 19px;"><b>Department:</b> Department of Electrical & Computer Engineering</p>
            <p style="font-size: 19px;"><b>Program:</b> B.E Tech(AI)</p>
            <p style="font-size: 19px;"><b>Supervisor:</b> Engr. Asad</p>
            <hr style="opacity: 0.2;">
            <p style="font-size: 17px;"><b>Team:</b> Amna Mudassar Ali, Fatima Arshad, Ayesha Bint e Israr, Tehreen Ramesha</p>
            <p style="font-size: 17px;"><b>Reg Numbers:</b> 016809, 012221, 012214, 012218</p>
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
        # Added alphabetical sorting for the massive city list
        selected_city = st.selectbox("TARGET AREA", sorted(list(LOCATIONS_PK.keys())))
    
    lat, lon = LOCATIONS_PK[selected_city]
    
    @st.cache_data(ttl=600)
    def fetch_weather(lat, lon):
        try:
            url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true&hourly=relative_humidity_2m,surface_pressure,cloudcover,rain&timezone=auto"
            return requests.get(url).json()
        except: return None

    data = fetch_weather(lat, lon)

    if data:
        h9, h3 = data['hourly']['relative_humidity_2m'][9], data['hourly']['relative_humidity_2m'][15]
        p9, p3 = data['hourly']['surface_pressure'][9], data['hourly']['surface_pressure'][15]
        c9, c3 = data['hourly']['cloudcover'][9]/12.5, data['hourly']['cloudcover'][15]/12.5
        rain_now = data['current_weather'].get('rain', 0)
        loc_enc = label_encoder.transform([selected_city])[0]
        input_data = np.array([[rain_now, h9, h3, p9, p3, c9, c3, loc_enc]])
        prob = ai_model.predict_proba(input_data)[0][1]
        prob = min(1.0, prob * 1.5) 

        st.markdown(f"## 🛰️ Monitored Feed: {selected_city} - {st.session_state.page}")

        if st.session_state.page == "Rain":
            fig = px.area(x=list(range(24)), y=data['hourly']['relative_humidity_2m'][:24])
            fig.update_traces(line_color='#add8e6') 
            fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(255,255,255,0.1)', font_color="#fffdd0")
            st.plotly_chart(fig, use_container_width=True)

        elif st.session_state.page == "Flood":
            fig = go.Figure(go.Indicator(mode="gauge+number", value=prob*100, gauge={'bar': {'color': "#add8e6"}}))
            fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', font_color="#fffdd0")
            st.plotly_chart(fig, use_container_width=True)

        elif st.session_state.page == "Satellite":
            st.map(pd.DataFrame({'lat': [lat], 'lon': [lon]}))

        elif st.session_state.page == "Economic":
            dynamic_risk = [prob*90, prob*60, prob*75]
            impact_df = pd.DataFrame({"Sector": ["Agri", "Urban", "Infra"], "Risk %": dynamic_risk})
            fig = px.bar(impact_df, x="Sector", y="Risk %", color_discrete_sequence=['#add8e6'], range_y=[0, 100])
            fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(255,255,255,0.1)', font_color="#fffdd0")
            st.plotly_chart(fig, use_container_width=True)
