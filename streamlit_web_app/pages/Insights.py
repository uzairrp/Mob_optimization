import pandas as pd
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt

st.title('Estadísticas Relevantes')

# Access the data stored in session state
data = st.session_state.data
# st.write(data.head())


# Top 20

st.write('Como haremos predicciones sobre los veinte trayectos con mas viajes, os presentamos cuáles son:')
# Grouping by origin city to find average number of journeys and travelers
data['pair'] = data.apply(lambda x: tuple(sorted([x['provincia_origen_name'], x['provincia_destino_name']])), axis=1)
top_pairs = data.groupby('pair')['viajes'].sum()
top_pairs = top_pairs.sort_values(ascending=False).head(20)

st.write(top_pairs)

# Weekday trends

st.write('A continuación tenemos una gráfica que muestra los viajes promedios por día de la semana. Podemos observar un pico claro (y lógico) en los viernes.')
# Datetime format for the column
data['day'] = pd.to_datetime(data['day'])

# Extract day of the week (0 = Monday, 6 = Sunday) and month
data['day_of_week'] = data['day'].dt.dayofweek
data['month'] = data['day'].dt.month

# Group by day of the week to find average journeys and travelers
daily_trends = data.groupby('day_of_week').agg(
    avg_viajes=('viajes', 'mean'),
)
# Rename day numbers to weekday names
day_names = {0: 'Monday', 1: 'Tuesday', 2: 'Wednesday', 3: 'Thursday', 4: 'Friday', 5: 'Saturday', 6: 'Sunday'}
daily_trends.index = daily_trends.index.map(day_names)

# Plot average journeys by day of the week
plt.figure(figsize=(10, 5))
daily_trends['avg_viajes'].plot(kind='bar', color='skyblue', label='Average Journeys')
plt.title('Average Journeys by Day of the Week')
plt.xlabel('Day of the Week')
plt.ylabel('Average Number of Journeys')
plt.xticks(rotation=45)
plt.legend()
st.pyplot(plt)


# Month date trends

st.write('Lo siguiente es una gráfica que muestra las 5 fechas con el promedio de viajes más alto. Estas fechas nos hacen pensar que se debe a los días de cobros salariales.')
# Extract the day of the month
data['day_of_month'] = data['day'].dt.day

# Group by day of the month to calculate average journeys and travelers
monthly_trends = data.groupby('day_of_month').agg(
    avg_viajes=('viajes', 'mean'),
)

# Sort by average journeys to get the top 7 days with the highest average journeys
top_days_viajes = monthly_trends.sort_values(by='avg_viajes', ascending=False).head(5)

# Plotting top 5 days of the month with the highest average journeys
plt.figure(figsize=(10, 5))
top_days_viajes['avg_viajes'].plot(kind='bar', color='skyblue', label='Average Journeys')
plt.title('Top 5 Days of the Month by Average Journeys')
plt.xlabel('Day of the Month')
plt.ylabel('Average Number of Journeys')
plt.xticks(rotation=0)
plt.legend()
st.pyplot(plt)


# Weekly/Monthly trends

st.write('Aumentamos la escala un poco y enfocamos en los patrones a niveles de semanas y meses. Podemos ver patrones muy claros.')
# Extract additional features: week, month, and year
data['week'] = data['day'].dt.isocalendar().week  # ISO week number
data['month'] = data['day'].dt.month
data['year'] = data['day'].dt.year

st.write('Desarrollo semanal')
# Aggregate data by week to observe weekly trends in journeys and travelers
weekly_trends = data.groupby(['year', 'week']).agg(
    weekly_viajes=('viajes', 'sum'),
).reset_index()
plt.figure(figsize=(12, 6))
# Combine year and week for x-axis labels
weekly_trends['year_week'] = weekly_trends['year'].astype(str) + '-W' + weekly_trends['week'].astype(str)
plt.plot(weekly_trends['year_week'], weekly_trends['weekly_viajes'], label='Weekly Journeys', color='skyblue')
plt.title('Weekly Trends in Journeys and Travelers')
plt.xlabel('Year-Week')
plt.ylabel('Total Count')
plt.xticks(rotation=90)  # Rotate x-axis labels for better readability
plt.legend()
plt.tight_layout()  # Adjust layout to make room for rotated labels
st.pyplot(plt)

st.write('Desarrollo mensual')
# Aggregate data by month to observe monthly trends in journeys and travelers
monthly_trends = data.groupby(['year', 'month']).agg(
    monthly_viajes=('viajes', 'sum'),
    monthly_viajeros=('viajeros', 'sum')
).reset_index()
# Plot monthly trends viajes
plt.figure(figsize=(12, 6))
# Combine year and month for x-axis labels
monthly_trends['year_month'] = monthly_trends['year'].astype(str) + '-' + monthly_trends['month'].astype(str).str.zfill(2)
plt.plot(monthly_trends['year_month'], monthly_trends['monthly_viajes'], label='Monthly Journeys', color='blue')
plt.title('Monthly Trends in Journeys and Travelers')
plt.xlabel('Year-Month')
plt.ylabel('Total Count')
plt.xticks(rotation=90)  # Rotate x-axis labels for better readability
plt.legend()
plt.tight_layout()  # Adjust layout to make room for rotated labels
st.pyplot(plt)


# Holiday trends

st.write('Ahora nos centramos en el impacto de los festivos sobre los viajes. Los festivos se han establecido internamente debido a la ausencia de algunos en el archivo proporcionado. Se pueden apreciar las repeticiones a una escala menor aquí también.')
# definimos nuestros propios festivos
holidays = ['2022-01-01', '2022-01-06', '2022-05-01', '2022-06-24', '2022-08-15', '2022-09-11', '2022-09-24', '2022-10-12', '2022-11-01', '2022-12-06', '2022-12-08', '2022-12-25', '2022-12-26',
            '2023-01-01', '2023-01-06', '2023-05-01', '2023-06-24', '2023-08-15', '2023-09-11', '2023-09-24', '2023-10-12', '2023-11-01', '2023-12-06', '2023-12-08', '2023-12-25', '2023-12-26',
            '2024-01-01', '2024-01-06', '2024-05-01', '2024-06-24', '2024-08-15', '2024-09-11', '2024-09-24', '2024-10-12', '2024-11-01', '2024-12-06', '2024-12-08', '2024-12-25', '2024-12-26']  # holiday dates
holidays = pd.to_datetime(holidays)

# Create a holiday flag in the data
data['is_holiday'] = data['day'].isin(holidays)

# Analyze the impact of holidays on traffic
holiday_trends = data[data['is_holiday']].groupby('day').agg(
    holiday_viajes=('viajes', 'sum'),
).reset_index()


plt.figure(figsize=(12, 6))
plt.plot(holiday_trends['day'], holiday_trends['holiday_viajes'], marker='o', color='blue', label='Journeys on Holidays', linewidth=2)
plt.title('Impact of Holidays on Journeys')
plt.xlabel('Holiday Date')
plt.ylabel('Total Count')
plt.xticks(rotation=45)
plt.legend()
plt.tight_layout()
st.pyplot(plt)


# Seasonal trends

st.write('Damos un paso más y miramos el comportamiento de los datos durante las diferentes estaciones del año.')
# Define a function to categorize months into seasons
def get_season(month):
    if month in [12, 1, 2]:
        return 'Winter'
    elif month in [3, 4, 5]:
        return 'Spring'
    elif month in [6, 7, 8]:
        return 'Summer'
    else:
        return 'Fall'

# Apply the function to create a 'season' column
data['season'] = data['day'].dt.month.apply(get_season)

# Group by city and season to calculate average journeys and travelers
seasonal_trends = data.groupby(['provincia_origen_name', 'season']).agg(
    avg_viajes=('viajes', 'mean'),
).reset_index()

# Calculate total journeys per city
total_journeys = data.groupby('provincia_origen_name').agg(
    total_viajes=('viajes', 'sum')
).reset_index()

# Get the top 10 cities with the largest number of journeys
top_10_cities = total_journeys.nlargest(10, 'total_viajes')['provincia_origen_name']

top_10_seasonal_trends = seasonal_trends[seasonal_trends['provincia_origen_name'].isin(top_10_cities)]


# Set the style for seaborn
sns.set_theme(style="whitegrid")

# Create a bar plot for average journeys by season for each of the top 10 cities
plt.figure(figsize=(14, 8))
sns.barplot(x='season', y='avg_viajes', hue='provincia_origen_name', data=top_10_seasonal_trends, palette='Set3')

# Set titles and labels
plt.title('Average Journeys by Season for Top 10 Cities')
plt.xlabel('Season')
plt.ylabel('Average Number of Journeys')
plt.legend(title='Origin City', bbox_to_anchor=(1.05, 1), loc='upper left')
st.pyplot(plt)

st.write('Podemos ver que en general siempre son las mismas provincias y que los números no tienen mucha desviación tampoco. Esto no lo es todo. Creemos que incorporando más información podemos sacar más cosas de estos datos como por ejemplo datos geográficos o información sobre los eventos que no incluyan los festivos.')
st.write('La continuación de este proyecto tiene muchas posibilidades intersantes y apostamos que NOMOS es el equipo para llevarla a cabo.')

