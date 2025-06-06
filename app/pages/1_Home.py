"""
1_Home.py  – hero avec logo + tagline + description animée
==========================================================

• Charge le CSS global (app/static/css/home.css)
• Injecte la section <hero> :
    - logo en BG
    - titre (tagline)
    - **nouvelle** description qui apparaît mot par mot
    - rangée de boutons (CTA)

Run:
    streamlit run app/pages/1_Home.py
"""
# ────────── 1. CONFIG (doit précéder tout le reste) ──────────
import streamlit as st
st.set_page_config(
    page_title="CCF – Home",
    page_icon="🌎",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ────────── 2. IMPORTS ──────────
from pathlib import Path
import base64
from app.components import navbar  # paquet interne (navbar horizontale)

# ────────── 3. NAVBAR ──────────
navbar.navbar(active="Home")

# ────────── 4. CHEMINS & CHARGEMENT DES ASSETS ──────────
BASE       = Path(__file__).resolve().parents[1]
css_file   = BASE / "static" / "css" / "home.css"
logo_file  = BASE / "static" / "assets" / "CCF_icone.jpg"

if not (css_file.exists() and logo_file.exists()):
    st.error("CSS or logo missing under app/static/")
    st.stop()

css_content = css_file.read_text(encoding="utf-8")
logo_b64    = base64.b64encode(logo_file.read_bytes()).decode()
logo_url    = f"data:image/jpg;base64,{logo_b64}"

# ────────── 5. TEXTE DE DESCRIPTION (résumé en 31 mots) ──────────
DESC = ("With 250,000 Canadian news articles and advanced machine-learning techniques, "
    "the CCF Project examines the evolution of climate-change media coverage across decades, regions, "
    "and news outlets throughout Canada, revealing the determinants shaping the representation and public understanding of climate change over time.")

# Pour conserver un espace entre les mots, ajoute un espace insécable (&nbsp;) à la fin de chaque span
WORD_SPANS = "".join(
    f'<span class="type-word" style="animation-delay:{4.5 + i*0.12:.2f}s">{w}&nbsp;</span>'
    for i, w in enumerate(DESC.split())
)

# ────────── 6. HTML DU HERO ──────────
HTML = f"""
<section class="hero">
   <img src="{logo_url}" class="bg-img" />
   <h1 class="tagline">Welcome to the CCF Project</h1>
   <p class="description">{WORD_SPANS}</p>

   <!-- ↓↓↓ HREF = véritables pages multipage, target=_self -->
   <div class="button-row">
      <a href="/Home"      class="cta-btn" target="_self">Home</a>
      <a href="/Database"  class="cta-btn" target="_self">The Database</a>
      <a href="/Idea"      class="cta-btn" target="_self">Project Idea</a>
      <a href="/Analysis"  class="cta-btn" target="_self">Some Analysis</a>
   </div>
</section>
"""

# ────────── 7. RENDU ──────────
st.markdown(f"<style>{css_content}</style>", unsafe_allow_html=True)
st.markdown(HTML, unsafe_allow_html=True)

