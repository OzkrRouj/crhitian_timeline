import streamlit as st
import pandas as pd
import altair as alt

st.set_page_config(page_title="Mi Aplicación", layout="wide")
# Datos corregidos
data = pd.DataFrame({
    "Año": [
        2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023,  # iPhones
        2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023  # Galaxy S
    ],
    "Modelo": [
        "iPhone", "iPhone 3G", "iPhone 3GS", "iPhone 4", "iPhone 4S", "iPhone 5", "iPhone 5S", "iPhone 6", "iPhone 6S",
        "iPhone 7", "iPhone 8", "iPhone X", "iPhone 11", "iPhone 12", "iPhone 13", "iPhone 14", "iPhone 15",
        "Galaxy S", "Galaxy S2", "Galaxy S3", "Galaxy S4", "Galaxy S5", "Galaxy S6", "Galaxy S7", "Galaxy S8",
        "Galaxy S9", "Galaxy S10", "Galaxy S20", "Galaxy S21", "Galaxy S22", "Galaxy S23"
    ],
    "Marca": ["Apple"] * 17 + ["Samsung"] * 14  # Se mantiene la misma longitud
})

# Inicializar session_state para el dominio del eje X
if "x_domain" not in st.session_state:
    st.session_state.x_domain = [data["Año"].min(), data["Año"].max()]

# Controles de zoom
zoom_factor = 0.2  # 20% de zoom
low, high = st.session_state.x_domain
center = (low + high) / 2
range_val = high - low

col1, col2, col3 = st.columns(3)
with col1:
    if st.button("Zoom In"):
        st.session_state.x_domain = [center - range_val * (1 - zoom_factor) / 2,
                                     center + range_val * (1 - zoom_factor) / 2]
with col2:
    if st.button("Reset Zoom"):
        st.session_state.x_domain = [data["Año"].min(), data["Año"].max()]
with col3:
    if st.button("Zoom Out"):
        st.session_state.x_domain = [center - range_val * (1 + zoom_factor) / 2,
                                     center + range_val * (1 + zoom_factor) / 2]

# Filtrar datos según el rango actual
filtered_data = data[(data["Año"] >= st.session_state.x_domain[0]) & (
    data["Año"] <= st.session_state.x_domain[1])]

# Crear gráfico con Altair (eje X cuantitativo para permitir zoom y desplazamiento)
chart = alt.Chart(filtered_data).mark_circle(size=100).encode(
    x=alt.X("Año:Q",
            scale=alt.Scale(domain=st.session_state.x_domain), title="Año de lanzamiento"),
    y=alt.Y("Marca:N", title="", axis=alt.Axis(labels=False)),  # Fija el eje Y
    color="Marca:N",
    tooltip=["Modelo", "Año"]
).properties(
    width=800,
    height=300,
    title="Lanzamiento de iPhones y Galaxy S por Año"
).configure_view(
    strokeOpacity=0
).interactive(False)

# Mostrar en Streamlit
st.title("Comparación de lanzamientos de iPhone y Galaxy S")


st.altair_chart(chart, use_container_width=True)
