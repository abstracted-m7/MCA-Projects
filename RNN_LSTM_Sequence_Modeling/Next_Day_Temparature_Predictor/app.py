import streamlit as st
import numpy as np
import joblib
from tensorflow.keras.models import load_model

st.title("Weather Temperature Prediction using RNN")

model = load_model("weather_model.h5", compile=False)
scaler = joblib.load("scaler.pkl")

st.write("Enter past 7 days temperature")

temps = []
for i in range(7):
    t = st.number_input(f"Day {i+1} Temperature")
    temps.append(t)

if st.button("Predict Tomorrow Temperature"):
    arr = np.array(temps).reshape(-1, 1)
    arr = scaler.transform(arr)
    arr = arr.reshape(1, 7, 1)
    pred = model.predict(arr)
    temp = scaler.inverse_transform(pred)
    st.success(f"Predicted Temperature: {temp[0][0]:.2f} °C")