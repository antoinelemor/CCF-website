# app/components/ui_utils.py  (ou l'endroit où vous avez mis hide_sidebar)

import streamlit as st

def hide_sidebar() -> None:
    """Masque totalement la sidebar *et tout contrôle permettant de l’ouvrir*."""
    st.markdown(
        """
        <style>
          /* 1 — bloc latéral + bandeau déco Streamlit */
          [data-testid="stSidebar"],
          [data-testid="stDecoration"]            {display:none !important;}

          /* 2 — marge de gauche réservée à la sidebar */
          [data-testid="stAppViewContainer"] > div:first-child {
              padding-left:0 !important;
          }

          /* 3 — tous les chevrons/​boutons qui ouvrent la sidebar
                 (différents sélecteurs pour couvrir plusieurs versions) */
          [data-testid="collapsedControl"],
          button[aria-label="Open sidebar"],
          button[aria-label="Close sidebar"],
          button[data-testid="stBaseButton-headerNoPadding"] {   /* ⬅︎ votre cas */
              display:none !important;
          }
        </style>
        """,
        unsafe_allow_html=True,
    )


