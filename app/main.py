# app/main.py  (entièrement réécrit)

import streamlit as st

st.set_page_config(
    page_title="CCF – Home",
    page_icon="🌎",
    layout="centered",
    initial_sidebar_state="collapsed"   # ← volet fermé par défaut
)

# Redirige immédiatement vers la vraie page d’accueil
st.switch_page("pages/1_Home.py")
