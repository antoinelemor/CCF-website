"""
Sticky “bare-buttons” navbar (Streamlit ≥ 1.31)
----------------------------------------------
• 100 % FIXED : reste visible quand on scrolle (position:fixed).
• Aucune barre apparente : seul le groupe de boutons est visible.
• Dégradé bleu → blanc, texte centré, gras, ombre, lift au survol.
• Icônes facultatives : mêmes couleurs que le bouton (héritent du texte).

Usage :
    from app.components import navbar
    navbar.navbar(active="Home")      # "Database", "Idea", "Analysis"
"""

from typing import Literal
import streamlit as st

PageName = Literal["Home", "Database", "Idea", "Analysis"]

# ------------------------------------------------------------------ CSS
NAV_CSS = """
<style>
/* ----- 0. réserver la place sous la nav fixe ------------------- */
body{padding-top:70px;}             /* évite que le contenu passe dessous */

/* ----- 1. conteneur fixe (invisible) ---------------------------- */
.sticky-nav{
  position:fixed;
  top:0;
  left:0;
  width:100%;
  display:flex;
  justify-content:center;
  z-index:1000;
  pointer-events:none;              /* conteneur intouchable      */
}

/* ----- 2. flexbox des boutons ----------------------------------- */
.navbar{
  display:flex;
  z-index:1001;
  gap:1.1rem;
  padding:.6rem 0;
  pointer-events:auto;              /* … mais les boutons, oui     */
}

/* ----- 3. bouton / lien ----------------------------------------- */
.nav-btn{
  display:inline-flex;              /* pour centrer texte+icône    */
  align-items:center;
  justify-content:center;
  gap:.35rem;                       /* espace icône / texte        */
  min-width:110px;
  padding:.48rem 1.25rem;
  font-weight:700;
  text-decoration:none;
  border-radius:999px;
  color:#0a2342 !important;         /* bleu foncé                  */
  background:linear-gradient(135deg,#3f83ff 0%,#ffffff 100%);
  box-shadow:0 2px 6px rgba(0,0,0,.18);
  transition:transform .18s ease, box-shadow .18s ease;
}

.nav-btn:hover{
  transform:translateY(-4px);
  box-shadow:0 4px 12px rgba(0,0,0,.28);
}

/* ----- 4. état actif -------------------------------------------- */
.nav-btn.active,
.nav-btn:disabled{
  pointer-events:none;
  background:linear-gradient(135deg,#184eea 0%,#c7d9ff 100%);
  color:#fff !important;
  box-shadow:0 3px 9px rgba(0,0,0,.25);
}
</style>
"""

# ------------------------------------------------------------------ MAIN
def navbar(active: PageName = "Home") -> None:
    """Affiche les boutons de navigation fixés en haut de l’écran."""
    st.markdown(NAV_CSS, unsafe_allow_html=True)

    pages = [
        ("Home",     "/Home",     "🏠"),
        ("Database", "/Database", "🗄️"),
        ("Idea",     "/Idea",     "💡"),
        ("Analysis", "/Analysis", "📊"),
    ]

    links_html = "".join(
        f'<a class="nav-btn {"active" if lbl==active else ""}" '
        f'href="{url}" target="_self">'
        f'{icon}<span>{lbl}</span></a>'
        for lbl, url, icon in pages
    )

    st.markdown(
        f'<div class="sticky-nav"><nav class="navbar">{links_html}</nav></div>',
        unsafe_allow_html=True,
    )
