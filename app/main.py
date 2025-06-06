import streamlit as st

# facultatif : config minimale
st.set_page_config(page_title="CCF – Home", page_icon="🌎", layout="centered")

# redirige vers la page d'accueil multipage
st.switch_page("pages/1_Home.py")
