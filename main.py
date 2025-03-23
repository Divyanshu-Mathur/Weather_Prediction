import streamlit as st
from tensorflow.keras.models import load_model
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
import os

# Load model
from tensorflow.keras.losses import MeanSquaredError, MeanAbsoluteError

custom_objects = {
    "mse": MeanSquaredError(),
    "mae": MeanAbsoluteError()
}
model = load_model("model.h5", custom_objects={"mse": MeanSquaredError()})


scaler = StandardScaler()
st.title("Weather Prediction")


option = st.radio("Select Prediction Type:", ("Day-wise", "Month-wise"))

if option == "Day-wise":
    day = st.number_input("Enter Day:", min_value=1, max_value=31, step=1)
    month = st.number_input("Enter Month:", min_value=1, max_value=12, step=1)
    year = st.number_input("Enter Year:", min_value=2020, max_value=2030, step=1)
    
    if st.button("Predict Weather"):
        input_data = np.array([[day, month, year]])
        print(input_data)
        input_scaled = scaler.fit_transform(input_data) 
        prediction = model.predict(input_scaled.reshape(-1,1,input_scaled.shape[1]))
        print(prediction)
        max_temp, min_temp, rain = prediction[0]
        
        st.write(f"### Weather on {day}-{month}-{year}")
        st.write(f"- **Max Temperature:** {max_temp:.2f}°C")
        st.write(f"- **Min Temperature:** {min_temp:.2f}°C")
        
        if rain > 2:
            st.write("- **Rainfall ** Yes")
        else:
            st.write("- **Rainfall ** No")

elif option == "Month-wise":
    month = st.number_input("Enter Month:", min_value=1, max_value=12, step=1)
    year = st.number_input("Enter Year:", min_value=2020, max_value=2030, step=1)
    
    if st.button("Show Graph"):
        days = np.arange(1, 32) 
        input_data = np.array([[day, month, year] for day in days])
        input_scaled = scaler.fit_transform(input_data)
        input_reshaped = input_scaled.reshape(-1, 1, input_scaled.shape[1])
        predictions = model.predict(input_reshaped)
        max_temps = predictions[:, 0]
        min_temps = predictions[:, 1]
        rainfall = predictions[:, 2]
        print(rainfall)
        rainfall_binary = np.where(rainfall > 2, 1, 0) 
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 10))
        bar_width = 0.35  # Width of each bar
        x = np.arange(len(days))
        ax1.bar(x - bar_width/2, max_temps, width=bar_width, color='r', alpha=0.6, label='Max Temp (°C)')
        ax1.bar(x + bar_width/2, min_temps, width=bar_width, color='b', alpha=0.6, label='Min Temp (°C)')
        ax1.set_xlabel("Day")
        ax1.set_ylabel("Temperature (°C)")
        ax1.set_title("Max and Min Temperatures")
        ax1.set_xticks(x)  # Set x-ticks to days
        ax1.set_xticklabels(days)  # Label x-ticks with day numbers
        ax1.legend(loc="upper left")

        ax2.bar(days, rainfall_binary, color='g', alpha=0.6, label='Rainfall > 0.5 mm')
        ax2.set_xlabel("Day")
        ax2.set_ylabel("Rainfall (Yes/No)")
        ax2.set_title("Rainfall ")
        ax2.set_yticks([0, 1])  
        ax2.set_yticklabels(["No", "Yes"])  # Label y-ticks as "No" and "Yes"
        ax2.legend(loc="upper left")

        plt.tight_layout()
    
    # Display the plot in Streamlit
        st.pyplot(fig)
