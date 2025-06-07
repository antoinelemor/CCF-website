"""
CCF ‑ Home page  – media‑logo edition
-------------------------------------
• même contenu qu’avant + apparition des logos des 20 médias
  (transparents, éparpillés aléatoirement derrière le logo CCF)
• tous les tempos restent centralisés dans ANIM
"""

from __future__ import annotations
import base64, html as esc, random, sys
from pathlib import Path
from typing import List, Dict

import streamlit as st
ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.components.navbar     import navbar
from app.components.ui_utils   import hide_sidebar

# ------------------------------------------------------------------ #
# 0.  Animation parameters (s)                                        #
# ------------------------------------------------------------------ #
ANIM = dict(
    logo_fade    = 1.0,
    tagline_wait = 1.0, tagline_fade = 1.2,
    desc_wait    = 1.2, word_step    = 0.10,
    cta_wait     = 0.2,  team_wait   = 0.2,
    member_step  = 0.25,
    media_step   = 0.12,          # <-- délai entre 2 logos
)

# ------------------------------------------------------------------ #
# 1.  Page config & assets                                            #
# ------------------------------------------------------------------ #
BASE_DIR   = Path(__file__).resolve().parents[1]
CSS_FILE   = BASE_DIR / "static/css/home.css"
LOGO_FILE  = BASE_DIR / "static/assets/CCF_icone.png"
MEDIA_DIR  = BASE_DIR / "static/assets/media"      # 20 logos

st.set_page_config("CCF – Home", "🌎", layout="centered",
                   initial_sidebar_state="collapsed")
navbar(active="Home")
hide_sidebar()

if not (CSS_FILE.exists() and LOGO_FILE.exists() and MEDIA_DIR.exists()):
    st.error("Missing assets"); st.stop()

# background CCF logo
logo_url = "data:image/png;base64," + base64.b64encode(
    LOGO_FILE.read_bytes()).decode()


# ------------------------------------------------------------------ #
# 2.  Media logos • positions stratifiées (grille + jitter)          #
# ------------------------------------------------------------------ #
import math, random

media_files = sorted(fp for fp in MEDIA_DIR.iterdir() if fp.is_file())
N = len(media_files)

# ── description + WORD_SPANS (inchangés) ───────────────────────────
DESC = ("With 250,000 Canadian news articles since 1978 and advanced "
        "machine-learning techniques, the CCF Project analyses how national "
        "climate-change media coverage has evolved across decades, regions "
        "and outlets.")
WORD_SPANS = "".join(
    f'<span class="type-word" '
    f'style="animation-delay:{ANIM['desc_wait']+i*ANIM['word_step']:.2f}s">'
    f'{esc.escape(w)}&nbsp;</span>' for i, w in enumerate(DESC.split())
)

# ── chronologie de l’apparition des logos ──────────────────────────
media_start = (ANIM["tagline_wait"] + ANIM["tagline_fade"]
               + ANIM["desc_wait"]  + ANIM["word_step"] * len(DESC.split())
               + ANIM["cta_wait"]   + ANIM["team_wait"] + 0.4)

# ── paramètres de placement ────────────────────────────────────────
COLS, ROWS = 5, 5      # 25 cases → répartition verticale + homogène
MARGIN_X   = 8         # %  (≥ demi-largeur max d’un logo sur mobile)
MARGIN_Y   = 6
HOLE_R2    = 20**2     # disque central un peu plus petit (logo CCF + tagline)
JITTER     = .30       # léger aléa pour casser la grille


rnd = random.Random(42)

# centres de chaque case
step_x = (100 - 2*MARGIN_X) / COLS
step_y = (100 - 2*MARGIN_Y) / ROWS
cells  = [(c, r) for r in range(ROWS) for c in range(COLS)]
rnd.shuffle(cells)                 # ordre pseudo-aléatoire reproductible

# ---------------------------------------------------------
# génération des positions en %  (≥ 4 logos entre 15 % et 30 %)
# ---------------------------------------------------------
TOP_BAND = (15, 30)      # % de hauteur
NEEDED_TOP = 4           # on veut au moins 4 logos visibles là-haut

positions: list[tuple[float, float]] = []
top_slots: list[tuple[float, float]] = []

for c, r in cells:
    if len(positions) == N:          # déjà 20 → stop
        break
    x = MARGIN_X + (c + 0.5) * step_x
    y = MARGIN_Y + (r + 0.5) * step_y
    if (x-50)**2 + (y-50)**2 < HOLE_R2:
        continue                     # trop près du centre
    dx = rnd.uniform(-JITTER, JITTER) * step_x
    dy = rnd.uniform(-JITTER, JITTER) * step_y
    x, y = x + dx, y + dy
    if TOP_BAND[0] <= y <= TOP_BAND[1] and len(top_slots) < NEEDED_TOP:
        top_slots.append((x, y))     # on met de côté jusqu’à 4 logos « haut »
    else:
        positions.append((x, y))

# insère en tête les 4 positions « haut »
positions = top_slots + positions
positions = positions[:N]            # garde exactement 20 positions


# ── HTML des logos ─────────────────────────────────────────────────
media_imgs = []
for idx, (fp, (x, y)) in enumerate(zip(media_files, positions)):
    b64 = base64.b64encode(fp.read_bytes()).decode()
    delay = media_start + idx * ANIM["media_step"]
    media_imgs.append(
        f'<img src="data:image/{fp.suffix.lstrip(".")};base64,{b64}" '
        f'class="media-logo" style="--delay:{delay:.2f}s; '
        f'left:{x:.2f}%; top:{y:.2f}%;" alt="{fp.stem}"/>'
    )



# ------------------------------------------------------------------ #
# 3.  Team members helper                                            #
# ------------------------------------------------------------------ #
TEAM: List[Dict[str, str]] = [
    dict(name="Alizée Pillod",  affil="Université de Montréal",
         photo=BASE_DIR/"static/assets/alizee.jpg",
         url="https://alizeepillod.com/"),
    dict(name="Antoine Lemor", affil="Université de Sherbrooke",
         photo=BASE_DIR/"static/assets/antoine.jpg",
         url="https://antoinelemor.github.io/"),
    dict(name="Matthew Taylor", affil="Université de Montréal",
         photo=BASE_DIR/"static/assets/matthew.jpeg",
         url="https://www.chairedemocratie.com/members/taylor-matthew/"),
]

def card(m: Dict[str, str]) -> str:
    """Retourne la carte HTML d’un membre avec photo cliquable."""
    if m["photo"].exists():
        img_b64 = base64.b64encode(m["photo"].read_bytes()).decode()
        img_tag = (f'<a href="{m["url"]}" target="_blank" class="member-photo">'
                   f'<img src="data:image/jpeg;base64,{img_b64}" alt="{m["name"]} photo"></a>')
    else:
        img_tag = ""
    return (f'<div class="member">{img_tag}'
            f'<a href="{m["url"]}" target="_blank" class="member-btn">{m["name"]}</a>'
            f'<p class="member-affil">{m["affil"]}</p></div>')



# ------------------------------------------------------------------ #
# 4.  Animated description                                           #
# ------------------------------------------------------------------ #


# ------------------------------------------------------------------ #
# 5.  Inject CSS (variables)                                         #
# ------------------------------------------------------------------ #
css_vars = ";".join(f"--{k}:{v}s" for k, v in ANIM.items())
st.markdown(
    f"<style>:root{{{css_vars}}}</style>",
    unsafe_allow_html=True,
)
st.markdown(f"<style>{CSS_FILE.read_text()}</style>", unsafe_allow_html=True)

# ------------------------------------------------------------------ #
# 6.  Final HTML                                                     #
# ------------------------------------------------------------------ #
st.markdown(
f"""
<section class="hero">

  <!-- background CCF logo -->
  <img src="{logo_url}" class="bg-img" />

  <!-- translucent media logos (behind everything) -->
  <div class="media-layer">
    {''.join(media_imgs)}
  </div>

  <!-- main headline -->
  <h1 class="tagline">Welcome to the CCF&nbsp;Project</h1>

  <!-- animated description -->
  <p class="description">{WORD_SPANS}</p>

  <!-- CTA buttons -->
  <div class="button-row">
    <a href="/Database" class="cta-btn" target="_self">The&nbsp;Database</a>
    <a href="/Idea"     class="cta-btn" target="_self">Project&nbsp;Idea</a>
    <a href="/Analysis" class="cta-btn" target="_self">Some&nbsp;Analysis</a>
  </div>

  <!-- team -->
  <h2 class="team-title">Project Members</h2>
  <div class="team-row">
    {''.join(card(m) for m in TEAM)}
  </div>

</section>
""",
unsafe_allow_html=True)
