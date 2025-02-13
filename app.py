import streamlit as st
from streamlit_timeline import st_timeline
from utils.data_loader import load_data

st.set_page_config(layout="wide")
st.title("Línea del Tiempo del Cristianismo")

# Cargar datos
df = load_data()
items = df.to_dict('records')

# Configurar grupos
groups = [
    {"id": 1, "content": "Dinastías y Emperadores Romanos"},
    {"id": 2, "content": "Eventos y Conflictos"},
    {"id": 3, "content": "Desarrollo del Cristianismo"},
    {"id": 4, "content": "Personajes Clave"},
    {"id": 5, "content": "Textos y Documentos"},
    {"id": 6, "content": "Controversias"}
]

# Mostrar timeline
timeline = st_timeline(
    items, groups=groups,
    options={
        "selectable": True,
        "multiselect": True,
        "zoomable": True,
        "verticalScroll": True,
        "stack": False,
        "height": 360,
        "margin": {"axis": 10},
        "groupHeightMode": "fixed",
        "orientation": {"axis": "top", "item": "top"}
    }
)

# Mostrar detalles
if timeline:
    st.subheader("Detalles del Evento")
    st.write(timeline["content"])
    st.write(f"Año: {timeline['start']}")

# import streamlit as st
# from streamlit_timeline import st_timeline

# st.set_page_config(layout="wide")
# st.title("Línea del Tiempo del Cristianismo")

# # Datos iniciales
# items = [
#     {"id": 1, "content": "Edicto de Milán", "start": "313"},
#     {"id": 2, "content": "Concilio de Nicea", "start": "325"}
# ]

# # Mostrar timeline
# timeline = st_timeline(items,
#                        options={
#                            "selectable": True,
#                            "multiselect": True,
#                            "zoomable": True,
#                            "verticalScroll": True,
#                            "stack": False,
#                            "height": 500,
#                            "margin": {"axis": 10},
#                            "groupHeightMode": "fixed",
#                            "orientation": {"axis": "top", "item": "top"}
#                        }
#                        )
# st.write("Evento seleccionado:", timeline)
