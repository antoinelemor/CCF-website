# ────────── 0. bootstrap  (do NOT move) ──────────
from ..bootstrap import * 

import streamlit as st
st.set_page_config(page_title="CCF – Database", page_icon="🌎",
                   layout="centered", initial_sidebar_state="collapsed")

from ..components import navbar
navbar.navbar(active="Database")

st.title("Database")
st.write("Content coming soon …")
