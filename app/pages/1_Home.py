"""
PROJECT
-------
CCF-Website

TITLE
-----
1_Home.py – Streamlit Home Page

MAIN OBJECTIVE
--------------
Render a hero section with:
    • blurred logo background
    • animated one-sentence description
    • call-to-action buttons
    • “Project Members” title + portraits (progressive fade-in)

A top navigation bar is injected (hidden on Home by the component logic).

Dependencies
------------
- streamlit ≥ 1.33
- pathlib    (std lib)
- base64     (std lib)

Author
------
Antoine Lemor
"""
from __future__ import annotations

import base64
from pathlib import Path
import sys                       # ← déjà présent, garde-le
from typing import List, Dict

# << bloc ROOT ⬇️ ajouté ici >>
ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.components.navbar import navbar
import streamlit as st


# ------------------------------------------------------------------ #
# 1. Streamlit page configuration                                    #
# ------------------------------------------------------------------ #
st.set_page_config(
    page_title="CCF – Home",
    page_icon="🌎",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# Inject (but hidden) navbar
navbar(active="Home")

# ------------------------------------------------------------------ #
# 2. Paths & external assets                                         #
# ------------------------------------------------------------------ #
BASE_DIR = Path(__file__).resolve().parents[1]
CSS_FILE = BASE_DIR / "static" / "css" / "home.css"
LOGO_FILE = BASE_DIR / "static" / "assets" / "CCF_icone.jpg"

if not (CSS_FILE.exists() and LOGO_FILE.exists()):
    st.error("Missing CSS or logo under app/static/")
    st.stop()

css_content = CSS_FILE.read_text(encoding="utf-8")
logo_b64 = base64.b64encode(LOGO_FILE.read_bytes()).decode()
logo_url = f"data:image/jpg;base64,{logo_b64}"

# ------------------------------------------------------------------ #
# 3. Project members data & helper                                   #
# ------------------------------------------------------------------ #
TEAM: List[Dict[str, str]] = [
    {
        "name": "Alizée Pillod",
        "affil": "Université de Montréal",
        "photo": BASE_DIR / "static" / "assets" / "alizee.jpg",
        "url": "https://alizeepillod.com/",
    },
    {
        "name": "Antoine Lemor",
        "affil": "Université de Sherbrooke",
        "photo": BASE_DIR / "static" / "assets" / "antoine.jpg",
        "url": "https://antoinelemor.github.io/",
    },
    {
        "name": "Matthew Taylor",
        "affil": "Université de Montréal",
        "photo": BASE_DIR / "static" / "assets" / "matthew.jpeg",
        "url": "https://www.chairedemocratie.com/members/taylor-matthew/",
    },
]


def build_member_card(member: Dict[str, str]) -> str:
    """Return HTML for a single team member."""
    if not member["photo"].exists():
        st.warning(f"Photo missing: {member['photo'].name}")
        img_src = ""
    else:
        img_src = (
            "data:image/jpeg;base64,"
            + base64.b64encode(member["photo"].read_bytes()).decode()
        )

    return (
        '<div class="member">'
        f'  <img src="{img_src}" alt="{member["name"]} portrait" />'
        f'  <a href="{member["url"]}" target="_blank" rel="noopener" '
        f'     class="member-btn">{member["name"]}</a>'
        f'  <p class="member-affil">{member["affil"]}</p>'
        '</div>'
    )



# ------------------------------------------------------------------ #
# 4. Animated one-sentence description                               #
# ------------------------------------------------------------------ #
DESC = (
    "With 250,000 Canadian news articles and advanced machine-learning "
    "techniques, the CCF Project examines the evolution of climate-change "
    "media coverage across decades, regions, and outlets, revealing the "
    "determinants shaping public understanding over time."
)
WORD_SPANS = "".join(
    f'<span class="type-word" style="animation-delay:{4.5 + i * 0.12:.2f}s">'
    f"{w}&nbsp;</span>"
    for i, w in enumerate(DESC.split())
)

# ------------------------------------------------------------------ #
# 5. Hero section HTML                                               #
# ------------------------------------------------------------------ #
HTML_HERO = f"""
<section class="hero">
  <!-- Background logo -->
  <img src="{logo_url}" class="bg-img" />

  <!-- Main headline -->
  <h1 class="tagline">Welcome to the CCF Project</h1>

  <!-- Animated description -->
  <p class="description">{WORD_SPANS}</p>

  <!-- CTA buttons -->
  <div class="button-row">
    <a href="/Database" class="cta-btn" target="_self">The Database</a>
    <a href="/Idea"     class="cta-btn" target="_self">Project Idea</a>
    <a href="/Analysis" class="cta-btn" target="_self">Some Analysis</a>
  </div>

  <!-- Project members -->
  <h2 class="team-title">Project Members</h2>
  <div class="team-row">
    {''.join(build_member_card(m) for m in TEAM)}
  </div>
</section>
"""

# ------------------------------------------------------------------ #
# 6. Render                                                          #
# ------------------------------------------------------------------ #
st.markdown(f"<style>{css_content}</style>", unsafe_allow_html=True)
st.markdown(HTML_HERO, unsafe_allow_html=True)
