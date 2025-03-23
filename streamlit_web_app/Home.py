import pandas as pd
import streamlit as st

# Set the page configuration
st.set_page_config(
    page_title="NOMOS Web App",
    page_icon=":earth_africa:",
    layout="centered",
    initial_sidebar_state="collapsed"  

)

# Display the header image
st.image("nomos_logo.jpeg", use_column_width=True)

st.title('CityFlow')
st.markdown('#### En esta aplicación web os presentamos los insights, el modelo y los resultados obtenidos.')
st.markdown('##### Miembros del equipo: Eneko Treviño, Marc Bacaicoa, Marc Riera, Ricard Segura y Uzair Ramzan.') 
st.write('Os queremos agradecer por esta oportunidad y para vuestra colaboración a lo largo del proyecto. Podeis seleccionar la sección que queráis visualizar usando el menú de la izquierda.')

# # Sidebar content
# st.sidebar.title("Menú")


st.session_state.data = pd.read_csv("mobility_data.csv")
