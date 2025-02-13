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


filtered_data = df[(df['start'] >= st.session_state.x_domain[0]) &
                   (df['start'] <= st.session_state.x_domain[1])]

# Crear selección con la nueva sintaxis
selection = alt.selection_point(
    name='event_selection',
    fields=['id'],
    on='click',
    empty=False
)


# Construir el gráfico
chart = alt.Chart(filtered_data).mark_circle(size=100).encode(
    x=alt.X('start:Q',
            scale=alt.Scale(domain=st.session_state.x_domain),
            title="Años"),
    y=alt.Y('group_name:N', title="", axis=None),
    color=alt.Color('group_name:N', legend=alt.Legend(title="Grupo")),
    tooltip=['content', 'start', 'description', 'group_name']
).add_params(
    selection
).properties(
    width=800,
    height=400,
    title=""
).interactive(False)

# Mostrar gráfico con manejo de selección
st.title("Timeline de Eventos Históricos")

with st.container():
    col_chart, col_controls = st.columns([7000, 1])  # Relación 4:1 de espacio

    with col_chart:
        # Mostrar el gráfico
        chart_key = "main_chart"
        st.altair_chart(
            chart,
            use_container_width=True,
            key=chart_key,
            on_select="rerun",
            selection_mode=[selection.name]
        )

    with col_controls:
        # Controles de zoom y selección

        zoom_factor = 0.2

        # Botón Zoom In
        if st.button("➕"):
            low, high = st.session_state.x_domain
            center = (low + high) / 2
            range_val = high - low
            st.session_state.x_domain = [
                center - range_val * (1 - zoom_factor)/2,
                center + range_val * (1 - zoom_factor)/2,
            ]
            st.rerun()

        # Botón Reset Zoom
        if st.button("🔄"):
            st.session_state.x_domain = [df['start'].min(), df['start'].max()]
            st.rerun()

        # Botón Zoom Out
        if st.button("➖"):
            low, high = st.session_state.x_domain
            center = (low + high) / 2
            range_val = high - low
            st.session_state.x_domain = [
                center - range_val * (1 + zoom_factor)/2,
                center + range_val * (1 + zoom_factor)/2,
            ]
            st.rerun()

        # Separador
        st.divider()

        # Botón Limpiar Selección
        if st.button("❌"):
            if chart_key in st.session_state:
                st.session_state[chart_key]['selection']['event_selection'] = []
            st.rerun()

# Manejar selección
st.subheader("Detalles del Evento")


chart_state = st.session_state[chart_key]


event_selected = None
# Extraer el ID del evento seleccionado
if chart_state['selection']['event_selection']:
    event_selected = chart_state['selection']['event_selection'][0]['id']

    # Filtrar el evento seleccionado
    evento_df = df[df['id'] == event_selected]

    if not evento_df.empty:
        # Mostrar detalles con formato
        st.write(f"**Evento:** {evento_df['content'].iloc[0]}")
        # Convertir a entero para quitar decimales
        st.write(f"**Año:** {int(evento_df['start'].iloc[0])}")
        st.write(f"**Descripción:** {evento_df['description'].iloc[0]}")
        # Usamos group_name en lugar de group
        st.write(f"**Grupo:** {evento_df['group_name'].iloc[0]}")
    else:
        st.warning("No se encontró el evento seleccionado")
else:
    st.info("Haz clic en un punto del gráfico para ver detalles")
