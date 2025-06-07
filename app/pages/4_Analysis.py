# --- make project root importable ---------------------------------
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from app.components.ui_utils import hide_sidebar
hide_sidebar()
# ------------------------------------------------------------------



import streamlit as st
st.set_page_config(
    page_title="CCF – Analysis",
    page_icon="🌎",
    layout="centered",
    initial_sidebar_state="collapsed",   # ← ok
)

from app.components import navbar
navbar(active="Analysis")  
hide_sidebar()

st.title("Analysis")
st.write("Content coming soon …")
