"""
CCF ‑ Home page
===============

All animation timings are now **centralised** in the `ANIM` dict below.
Tweak only these numbers to speed‑up / slow‑down the whole intro.

Dependencies
------------
streamlit ≥ 1.33
"""

from __future__ import annotations
import base64, sys, html as esc
from pathlib import Path
from typing import List, Dict
import streamlit as st
ROOT = Path(__file__).resolve().parents[2]   # dossier racine du projet
if str(ROOT) not in sys.path:                # ← ajoute-le au PYTHONPATH
    sys.path.insert(0, str(ROOT))
from app.components.navbar import navbar     # project import
from app.components.ui_utils import hide_sidebar


# ------------------------------------------------------------------ #
# 0 .  PARAMETERS  (edit here)                                       #
# ------------------------------------------------------------------ #
ANIM = dict(                 # second unit everywhere
    logo_fade    = 1.0,      # duration of the BG‑logo “appear‑then‑dim”
    tagline_wait = 1.0,      # delay before tagline starts fading‑in
    tagline_fade = 1.2,      # duration of tagline fade‑in
    desc_wait    = 1.2,      # delay before description starts
    word_step    = 0.10,     # gap between successive words
    cta_wait     = 0.2,      # delay *after* desc until CTA buttons
    team_wait    = 0.2,      # delay after CTA until team title
    member_step  = 0.25,     # gap between member cards
)

# ------------------------------------------------------------------ #
# 1 .  Page configuration & assets                                   #
# ------------------------------------------------------------------ #
BASE_DIR  = Path(__file__).resolve().parents[1]
CSS_FILE  = BASE_DIR / "static/css/home.css"
LOGO_FILE = BASE_DIR / "static/assets/CCF_icone.png"

st.set_page_config("CCF – Home", "🌎", layout="centered",
                   initial_sidebar_state="collapsed")
navbar(active="Home")
hide_sidebar()

if not (CSS_FILE.exists() and LOGO_FILE.exists()):
    st.error("Missing CSS or logo in app/static/"); st.stop()

# Base‑64 logo
logo_url = (
    "data:image/png;base64,"
    + base64.b64encode(LOGO_FILE.read_bytes()).decode()
)

# Inject CSS **once**, passing animation variables through CSS custom props
css_vars = ";".join(f"--{k}:{v}s" for k, v in ANIM.items())
st.markdown(
    f"<style>:root{{{css_vars}}}{CSS_FILE.read_text(encoding='utf‑8')}</style>",
    unsafe_allow_html=True,
)

# ------------------------------------------------------------------ #
# 2 .  Team members                                                  #
# ------------------------------------------------------------------ #
TEAM: List[Dict[str, str]] = [
    {
        "name": "Alizée Pillod",
        "affil": "Université de Montréal",
        "photo": BASE_DIR / "static/assets/alizee.jpg",
        "url": "https://alizeepillod.com/",
    },
    {
        "name": "Antoine Lemor",
        "affil": "Université de Sherbrooke",
        "photo": BASE_DIR / "static/assets/antoine.jpg",
        "url": "https://antoinelemor.github.io/",
    },
    {
        "name": "Matthew Taylor",
        "affil": "Université de Montréal",
        "photo": BASE_DIR / "static/assets/matthew.jpeg",
        "url": "https://www.chairedemocratie.com/members/taylor-matthew/",
    },
]


def member_card(m: Dict[str, str]) -> str:
    if not m["photo"].exists():
        img_src = ""
    else:
        img_src = (
            "data:image/jpeg;base64,"
            + base64.b64encode(m["photo"].read_bytes()).decode()
        )
    return (
        '<div class="member">'
        f'  <img src="{img_src}" alt="{m["name"]} portrait" />'
        f'  <a href="{m["url"]}" target="_blank" rel="noopener" '
        f'     class="member-btn">{m["name"]}</a>'
        f'  <p class="member-affil">{m["affil"]}</p>'
        '</div>'
    )


# ------------------------------------------------------------------ #
# 3 .  Animated description (word‑by‑word)                           #
# ------------------------------------------------------------------ #
DESC = (
    "With 250,000 Canadian news articles since 1978 and advanced machine‑"
    "learning techniques, the CCF Project analyses how national climate‑"
    "change media coverage has evolved across decades, regions and outlets."
)

WORD_SPANS = "".join(
    f'<span class="type-word" style="animation-delay:{ANIM["desc_wait"] + i*ANIM["word_step"]:.2f}s">'
    f"{esc.escape(w)}&nbsp;</span>"
    for i, w in enumerate(DESC.split())
)

# ------------------------------------------------------------------ #
# 4 .  Final HTML / render                                           #
# ------------------------------------------------------------------ #
st.markdown(
    f"""
<section class="hero">
  <img src="{logo_url}" class="bg-img" />

  <h1 class="tagline">Welcome to the CCF Project</h1>

  <p class="description">{WORD_SPANS}</p>

  <div class="button-row">
    <a href="/Database" class="cta-btn" target="_self">The Database</a>
    <a href="/Idea"     class="cta-btn" target="_self">Project Idea</a>
    <a href="/Analysis" class="cta-btn" target="_self">Some Analysis</a>
  </div>

  <h2 class="team-title">Project Members</h2>
  <div class="team-row">
    {''.join(member_card(m) for m in TEAM)}
  </div>
</section>
""",
    unsafe_allow_html=True,
)
