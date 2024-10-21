import time
import pandas as pd
import os
import streamlit as st
import seaborn as sns
import plotly.express as px


json_file_path = os.path.join("data", "data_base_final.json")
df = pd.read_json(json_file_path)


col1, col2, col3 = st.columns(3)

df['price'] = df['price'].replace({'\u202f': '', ' CFA': ''}, regex=True).astype(float)

st.sidebar.title("Sommaire")

col3.button('Press Me')

with col1:
    st.header("Première colonne")
    st.dataframe(df.head())


with col2:
    st.header("Deuxième colonne")
    
    chosen = st.radio(
        'Choisissez une option :',
        ['choix1', 'choix 2', 'choix restant', 'le surplus']
    )
    st.write(f"Réponse : {chosen}")

lastest=st.empty()
bar=st.progress(0)
for i in range(100):
    lastest.text(f"interation numero {i}")
    bar.progress(i+1)
    time.sleep(0.2)
