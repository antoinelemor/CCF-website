# --- make project root importable ---------------------------------
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]    # dossier racine du dépôt
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
# ------------------------------------------------------------------


import streamlit as st
st.set_page_config(page_title="CCF – Analysis", page_icon="🌎",
                   layout="centered", initial_sidebar_state="collapsed")

from app.components import navbar
navbar(active="Analysis")  

st.title("Analysis")
st.write("Content coming soon …")
