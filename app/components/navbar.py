"""
Navbar horizontale basée sur st.page_link
-----------------------------------------
Compatible Streamlit ≥ 1.31
"""

import streamlit as st
from typing import Literal

PageName = Literal["Home", "Database", "Idea", "Analysis"]

def navbar(active: PageName = "Home") -> None:
    """Affiche une barre de navigation en haut de la page."""
    cols = st.columns(4, gap="small")
    pages = [
        ("Home",     "pages/1_Home.py"),
        ("Database", "pages/2_Database.py"),
        ("Idea",     "pages/3_Idea.py"),
        ("Analysis", "pages/4_Analysis.py"),
    ]
    for col, (label, path) in zip(cols, pages):
        with col:
            st.page_link(
                path, label=label, icon=None,
                disabled=(label == active),
                use_container_width=True,
            )
