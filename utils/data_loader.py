import json
import pandas as pd
import streamlit as st


@st.cache_data
def load_data():
    with open('data/timeline_data.json', encoding='utf-8') as f:
        data = json.load(f)
    return pd.DataFrame(data)
