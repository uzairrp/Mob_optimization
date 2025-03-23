import streamlit as st
import pickle
import pandas as pd
import plotly.express as px
from lightgbm import LGBMRegressor
from datetime import datetime

# Load data, model, and encoders
with open('model_test_data_encoders.pkl', 'rb') as file:
    saved_data = pickle.load(file,encoding="latin1")

model = saved_data["model"]
province_encoder = saved_data["province_encoder"]
weather_encoder = saved_data["weather_encoder"]
holyday_type_encoder = saved_data["holyday_type_encoder"]
preciptype_encoder = saved_data["preciptype_encoder"]

# Valid province pairs
province_pairs = [
    (29, 46), (7, 20), (7, 44), (22, 29), (1, 31),
    (11, 47), (14, 37), (1, 47), (17, 42), (29, 41),
    (7, 27), (23, 42), (17, 32), (21, 32), (24, 50),
    (24, 27), (5, 16), (13, 46), (8, 10), (3, 8)
]

# Añadir los pares invertidos
reversed_pairs = [(dest, origin) for origin, dest in province_pairs]
all_pairs = province_pairs + reversed_pairs

# Decodificar números de provincias en nombres para la selección
decoded_pairs = [
    (province_encoder.inverse_transform([origin])[0], province_encoder.inverse_transform([dest])[0])
    for origin, dest in all_pairs
]

st.title("Página de Predicción del Modelo ML")

# Selector de fecha para año, mes y día
st.subheader("Selecciona una fecha")
selected_date = st.date_input("Elige una fecha")
year, month, day = selected_date.year, selected_date.month, selected_date.day

# Tipo de festivo
holiday_type = st.selectbox("Tipo de dia festivo", holyday_type_encoder.classes_)

# Calcular is_holiday basado en holiday_type
is_holiday = 0 if holiday_type == "Ninguno" else 1

# Determinar si la fecha seleccionada es fin de semana
is_weekend = int(selected_date.weekday() >= 5)

# Entrada del usuario para el par de provincias válido
st.subheader("Selecciona un viaje para hacer la predicción")
selected_pair = st.selectbox("Elige un par válido de provincias", decoded_pairs)
provincia_origen_name, provincia_destino_name = selected_pair



# Condiciones meteorológicas
st.subheader("Condiciones meteorológicas")
temp = st.slider("Temperatura (°C)", min_value=0, max_value= 50, value=20)
cloudcover = st.slider("Cobertura nubosa (%)", min_value=0, max_value=100, value=0)
precip = st.slider("Precipitación (mm)", min_value=0, max_value=100, value=0)
conditions = st.selectbox("Condiciones meteorológicas", weather_encoder.classes_)


# Hacer una predicción
if st.button("Predecir"):
    # Recodificar los nombres seleccionados de provincias a números
    provincia_origen_encoded = province_encoder.transform([provincia_origen_name])[0]
    provincia_destino_encoded = province_encoder.transform([provincia_destino_name])[0]
    holiday_type_encoded = holyday_type_encoder.transform([holiday_type])[0]
    preciptype_encoded = 3
    conditions_encoded = weather_encoder.transform([conditions])[0]

    # Preparar datos de entrada
    input_data = pd.DataFrame([{
        "provincia_origen_name": provincia_origen_encoded,
        "provincia_destino_name": provincia_destino_encoded,
        "holiday_type": holiday_type_encoded,
        "is_holiday": is_holiday,
        "temp": temp,
        "cloudcover": cloudcover,
        "precip": precip,
        "preciptype": preciptype_encoded,
        "conditions": conditions_encoded,
        "is_weekend": is_weekend,
        "year": year,
        "month": month,
        "day": day
    }])

    # Realizar la predicción
    prediction = model.predict(input_data)[0]
    st.success(f"El valor predicho es: {prediction:.2f}")