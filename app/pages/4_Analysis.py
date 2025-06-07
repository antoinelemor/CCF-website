# 4_Analysis.py
# ────────────────────────────────────────────────────────────────
import sys
from pathlib import Path

# --- rendre le projet importable (OK : n’utilise pas Streamlit) --
ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

# --- 1️⃣  PREMIÈRE commande Streamlit ----------------------------
import streamlit as st
st.set_page_config(
    page_title="CCF – Analysis",
    page_icon="🌎",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# --- 2️⃣  Maintenant on peut utiliser des helpers Streamlit -------
from app.components.ui_utils import hide_sidebar
from app.components import navbar

hide_sidebar()          # ← appelle st.markdown → maintenant autorisé
navbar(active="Analysis")

# --- 3️⃣  Contenu de la page -------------------------------------
st.title("Analysis")
st.write("Content coming soon …")
