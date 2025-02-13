import streamlit as st
import pandas as pd
import altair as alt
from utils.data_loader import load_data  # Asegúrate de que la ruta es correcta

# Configuración de la página
st.set_page_config(page_title="Timeline de Eventos Históricos", layout="wide")

# Cargar la data
df = load_data()

# Convertir la columna 'start' a numérica (ignoramos 'end' para la representación)
df['start'] = pd.to_numeric(df['start'], errors='coerce')

# Definir los nombres de cada grupo
groups = [
    {"id": 1, "content": "Emperadores Romanos"},
    {"id": 2, "content": "Eventos y Conflictos"},
    {"id": 3, "content": "Desarrollo del Cristianismo"},
    {"id": 4, "content": "Personajes Clave"},
    {"id": 5, "content": "Textos y Documentos"},
    {"id": 6, "content": "Controversias"}
]

# Crear un diccionario para mapear el id del grupo con su nombre
group_mapping = {group["id"]: group["content"] for group in groups}

# Agregar una columna nueva con el nombre del grupo
df['group_name'] = df['group'].map(group_mapping)

# Inicializar el dominio del eje X en el session_state
if "x_domain" not in st.session_state:
    st.session_state.x_domain = [df['start'].min(), df['start'].max()]

# Controles de zoom
zoom_factor = 0.2  # 20% de zoom
low, high = st.session_state.x_domain
center = (low + high) / 2
range_val = high - low

col1, col2, col3 = st.columns(3)
with col1:
    if st.button("Zoom In"):
        st.session_state.x_domain = [
            center - range_val * (1 - zoom_factor) / 2,
            center + range_val * (1 - zoom_factor) / 2,
        ]
with col2:
    if st.button("Reset Zoom"):
        st.session_state.x_domain = [df['start'].min(), df['start'].max()]
with col3:
    if st.button("Zoom Out"):
        st.session_state.x_domain = [
            center - range_val * (1 + zoom_factor) / 2,
            center + range_val * (1 + zoom_factor) / 2,
        ]

# Filtrar datos según el rango actual del eje X
filtered_data = df[(df['start'] >= st.session_state.x_domain[0]) &
                   (df['start'] <= st.session_state.x_domain[1])]

# Crear gráfico usando únicamente círculos que representan el inicio de cada evento
chart = alt.Chart(filtered_data).mark_circle(size=100).encode(
    x=alt.X('start:Q',
            scale=alt.Scale(domain=st.session_state.x_domain),
            title="Años"),
    y=alt.Y('group_name:N', title="", axis=None),
    color=alt.Color('group_name:N', legend=alt.Legend(title="Grupo")),
    tooltip=['content', 'start', 'description', 'group_name']
).properties(
    width=800,
    height=400,
    title="Timeline de Eventos Históricos"
).configure_view(
    strokeOpacity=0
).interactive(False)

# Título y despliegue del gráfico en Streamlit
st.title("Timeline de Eventos Históricos")
st.altair_chart(chart, use_container_width=True)

st.subheader("Detalles del Evento")
