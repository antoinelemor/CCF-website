# --- make project root importable ---------------------------------
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
# ------------------------------------------------------------------



import streamlit as st
st.set_page_config(page_title="CCF – Database", page_icon="🌎",
                   layout="centered", initial_sidebar_state="collapsed")

from app.components import navbar
navbar(active="Database")  

st.title("Database")
st.write("Content coming soon …")
