import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import LabelEncoder

# 1. LOAD AND PREPARE DATA
df = pd.read_csv('weatherAUS.csv')

# Use only the columns you requested
cols = ['Date', 'Location', 'Rainfall', 'Humidity9am', 'Humidity3pm',
        'Pressure9am', 'Pressure3pm', 'Cloud9am', 'Cloud3pm', 'RainTomorrow']
df = df[cols]

# 2. DERIVE AWI (Antecedent Wetness Index)
df['Date'] = pd.to_datetime(df['Date'])
df = df.sort_values(['Location', 'Date'])
df['Rainfall_Clean'] = df['Rainfall'].fillna(0)
df['AWI'] = df.groupby('Location')['Rainfall_Clean'].transform(lambda x: x.rolling(window=7, min_periods=1).sum())

# 3. PREPARE FOR MODEL TRAINING
df = df.dropna(subset=['RainTomorrow'])
df['Target'] = df['RainTomorrow'].map({'No': 0, 'Yes': 1})

# Encode Location names to numbers
le = LabelEncoder()
df['Loc_Enc'] = le.fit_transform(df['Location'])

# Features list
features_list = ['Rainfall_Clean', 'Humidity9am', 'Humidity3pm', 'Pressure9am',
                 'Pressure3pm', 'Cloud9am', 'Cloud3pm', 'AWI', 'Loc_Enc']
X = df[features_list]
y = df['Target']

# Handle missing data
imputer = SimpleImputer(strategy='median')
X_imputed = imputer.fit_transform(X)

# 4. SPLIT DATA (80% Train, 20% Test)
X_train, X_test, y_train, y_test = train_test_split(X_imputed, y, test_size=0.2, random_state=42)

# 5. TRAIN MODEL
print("Training model... please wait.")
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)
print("Model trained successfully on 80% of the data.\n")

# 6. INTERACTIVE INPUT SECTION
print("--- FLOOD DETECTION SYSTEM: MANUAL INPUT ---")

def get_manual_input():
    try:
        loc_name = input(f"Enter Location (e.g., Albury, Darwin, Sydney): ")
        # Handle location encoding
        if loc_name in le.classes_:
            loc_enc = le.transform([loc_name])[0]
        else:
            print(f"Location not recognized. Using default encoding.")
            loc_enc = 0

        rain_today = float(input("Enter Rainfall today (mm): "))
        h9 = float(input("Enter Humidity at 9am (%): "))
        h3 = float(input("Enter Humidity at 3pm (%): "))
        p9 = float(input("Enter Pressure at 9am (hPa): "))
        p3 = float(input("Enter Pressure at 3pm (hPa): "))
        c9 = float(input("Enter Cloud cover at 9am (0-8): "))
        c3 = float(input("Enter Cloud cover at 3pm (0-8): "))
        awi = float(input("Enter AWI (Total rain in last 7 days in mm): "))

        # Create input array
        user_data = np.array([[rain_today, h9, h3, p9, p3, c9, c3, awi, loc_enc]])

        # Predict
        prob = model.predict_proba(user_data)
        rain_prob = prob[0][1]
        confidence = np.max(prob[0])

        # Determine Wetness State
        if awi > 100:
            wet_state = "Saturated"
        elif awi > 30:
            wet_state = "Moderately Wet"
        else:
            wet_state = "Dry"

        # Display Results
        print("\n--- SYSTEM OUTPUT ---")
        print(f"Rain Probability Tomorrow: {rain_prob:.2f} ({(rain_prob*100):.1f}%)")
        print(f"Wetness State: {wet_state}")
        print(f"Confidence Score: {confidence:.2f}")

    except ValueError:
        print("Invalid input! Please enter numerical values for the weather data.")

# Call the function to ask for your data
get_manual_input()
