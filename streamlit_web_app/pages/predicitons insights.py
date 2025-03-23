import pandas as pd
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt

# Título de la aplicación
st.title('Análisis de Predicciones de Viajes')

# Carga de datos
@st.cache
def load_data():
    data = pd.read_csv('predictions.csv')
    data['pair'] = data.apply(lambda x: tuple(sorted([x['provincia_origen_name'], x['provincia_destino_name']])), axis=1)
    data['date'] = pd.to_datetime(data[['year', 'month', 'day']])
    return data

data = load_data()

# Top 20 trayectos
st.write('Los 20 trayectos con más viajes predichos:')
top_pairs = data.groupby('pair')['predicted_travels'].sum().sort_values(ascending=False).head(20)
st.write(top_pairs)

# Tendencias por día de la semana
st.write('Viajes promedio por día de la semana:')
data['day_of_week'] = data['date'].dt.dayofweek
day_names = {0: 'Monday', 1: 'Tuesday', 2: 'Wednesday', 3: 'Thursday', 4: 'Friday', 5: 'Saturday', 6: 'Sunday'}
data['day_of_week_name'] = data['day_of_week'].map(day_names)

daily_trends = data.groupby('day_of_week_name')['predicted_travels'].mean()
plt.figure(figsize=(10, 5))
daily_trends.plot(kind='bar', color='skyblue')
plt.title('Viajes Promedio por Día de la Semana')
plt.xlabel('Día de la Semana')
plt.ylabel('Viajes Promedio')
plt.xticks(rotation=45)
st.pyplot(plt)

# Tendencias por día del mes
st.write('Las 5 fechas con el promedio de viajes más alto:')
data['day_of_month'] = data['date'].dt.day
monthly_trends = data.groupby('day_of_month')['predicted_travels'].mean()
top_days = monthly_trends.sort_values(ascending=False).head(5)

plt.figure(figsize=(10, 5))
top_days.plot(kind='bar', color='skyblue')
plt.title('Top 5 Días del Mes por Viajes Promedio')
plt.xlabel('Día del Mes')
plt.ylabel('Viajes Promedio')
st.pyplot(plt)

# Tendencias semanales y mensuales
st.write('Tendencias Semanales y Mensuales:')
data['week'] = data['date'].dt.isocalendar().week
weekly_trends = data.groupby(['year', 'week'])['predicted_travels'].sum().reset_index()
weekly_trends['year_week'] = weekly_trends['year'].astype(str) + '-W' + weekly_trends['week'].astype(str)

plt.figure(figsize=(12, 6))
plt.plot(weekly_trends['year_week'], weekly_trends['predicted_travels'], label='Viajes Semanales', color='skyblue')
plt.title('Tendencias Semanales en Viajes')
plt.xlabel('Semana del Año')
plt.ylabel('Viajes Totales')
plt.xticks(rotation=90)
st.pyplot(plt)

monthly_trends = data.groupby(['year', 'month'])['predicted_travels'].sum().reset_index()
monthly_trends['year_month'] = monthly_trends['year'].astype(str) + '-' + monthly_trends['month'].astype(str).str.zfill(2)

plt.figure(figsize=(12, 6))
plt.plot(monthly_trends['year_month'], monthly_trends['predicted_travels'], label='Viajes Mensuales', color='blue')
plt.title('Tendencias Mensuales en Viajes')
plt.xlabel('Mes del Año')
plt.ylabel('Viajes Totales')
plt.xticks(rotation=90)
st.pyplot(plt)

# Análisis por estaciones
st.write('Tendencias por Estaciones del Año:')
def get_season(month):
    if month in [12, 1, 2]:
        return 'Invierno'
    elif month in [3, 4, 5]:
        return 'Primavera'
    elif month in [6, 7, 8]:
        return 'Verano'
    else:
        return 'Otoño'

data['season'] = data['month'].apply(get_season)
seasonal_trends = data.groupby(['provincia_origen_name', 'season'])['predicted_travels'].mean().reset_index()
top_cities = data.groupby('provincia_origen_name')['predicted_travels'].sum().nlargest(10).index

top_seasonal_trends = seasonal_trends[seasonal_trends['provincia_origen_name'].isin(top_cities)]

sns.set_theme(style="whitegrid")
plt.figure(figsize=(14, 8))
sns.barplot(x='season', y='predicted_travels', hue='provincia_origen_name', data=top_seasonal_trends, palette='Set3')
plt.title('Viajes Promedio por Estación para las 10 Principales Provincias')
plt.xlabel('Estación')
plt.ylabel('Viajes Promedio')
st.pyplot(plt)

st.write('Esta página analiza predicciones y patrones clave de las predicciones obtenidas en los datos.')


# Filtros interactivos
st.sidebar.header('Filtros de Provincias')
provincia_origen = st.sidebar.selectbox('Selecciona la Provincia de Origen:', data['provincia_origen_name'].unique())
provincia_destino = st.sidebar.selectbox('Selecciona la Provincia de Destino:', data['provincia_destino_name'].unique())

# Filtrar datos según las selecciones
filtered_data = data[(data['provincia_origen_name'] == provincia_origen) & 
                     (data['provincia_destino_name'] == provincia_destino)]

# Verificar si hay datos para las selecciones
if filtered_data.empty:
    st.write(f"No hay datos para los viajes desde {provincia_origen} hasta {provincia_destino}.")
else:
    # Gráfico de viajes a lo largo del tiempo
    st.subheader(f"Viajes Predichos desde {provincia_origen} hasta {provincia_destino}")
    plt.figure(figsize=(12, 6))
    plt.plot(filtered_data['date'], filtered_data['predicted_travels'], marker='o', linestyle='-', color='skyblue')
    plt.title(f"Viajes Predichos \n{provincia_origen} → {provincia_destino}")
    plt.xlabel("Fecha")
    plt.ylabel("Viajes Predichos")
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(plt)



