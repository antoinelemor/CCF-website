"""
Sticky buttons navbar – visible partout et pendant le scroll
Compatible Streamlit ≥ 1.25
"""

from typing import Literal
import streamlit as st

PageName = Literal["Home", "Database", "Idea", "Analysis"]

NAV_CSS = """
<style>
body{padding-top:74px;}  /* réserve la hauteur de la nav fixe              */

.sticky-nav{
  position:fixed; top:0; left:0; width:100%;
  display:flex; justify-content:center;
  z-index:3000;                /* passe devant tout le reste               */
  pointer-events:none;         /* conteneur intouchable                    */
  user-select:none;
}

.navbar{
  display:flex; gap:1rem; padding:.55rem 0;
  pointer-events:auto;        /* réactive les liens                        */
}

.nav-btn{
  display:inline-flex; align-items:center; justify-content:center; gap:.3rem;
  min-width:110px; padding:.45rem 1.2rem;
  font-weight:700; border-radius:999px; text-decoration:none;
  background:linear-gradient(135deg,#3f83ff 0%,#ffffff 100%);
  color:#0a2342 !important; box-shadow:0 2px 6px rgba(0,0,0,.18);
  transition:transform .18s, box-shadow .18s;
}

.nav-btn:hover{
  transform:translateY(-3px); box-shadow:0 4px 12px rgba(0,0,0,.28);
}

.nav-btn.active,
.nav-btn:disabled{
  pointer-events:none;
  background:linear-gradient(135deg,#184eea 0%,#c7d9ff 100%);
  color:#fff !important; box-shadow:0 3px 9px rgba(0,0,0,.25);
}
</style>
"""

def navbar(active: PageName = "Home") -> None:
    """Injecte la barre de navigation collante."""
    st.markdown(NAV_CSS, unsafe_allow_html=True)

    pages = [
        ("Home",     "/Home",     "🏠"),
        ("Database", "/Database", "🗄️"),
        ("Idea",     "/Idea",     "💡"),
        ("Analysis", "/Analysis", "📊"),
    ]

    buttons = "".join(
        f'<a class="nav-btn {"active" if lbl==active else ""}" '
        f'href="{url}" target="_self">{icon}<span>{lbl}</span></a>'
        for lbl, url, icon in pages
    )

    st.markdown(
        f'<div class="sticky-nav"><nav class="navbar">{buttons}</nav></div>',
        unsafe_allow_html=True,
    )
