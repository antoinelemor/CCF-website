"""
Database page
-------------
1. Sticky navbar (component)
2. Scrolling banner of outlet logos
3. Title ▸ buttons ▸ description (word-by-word)
4. ECharts in place – no full page reload
"""
from __future__ import annotations
import sys
from pathlib import Path

# ─────────────────── 1.  rendre la racine importable ──────────────────
# /mount/src/ccf-website/app/pages/2_Database.py
#   ↑            ↑            ↑
#   pages ← app ← racine  → on monte de 3 niveaux
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))          # AUCUN import « app. » avant ceci !

# ─────────────────── 2.  imports projet & tiers ───────────────────────
from app.components.navbar import navbar
from app.components.ui_utils import hide_sidebar

import json, html as esc, base64
import pandas as pd
import streamlit as st
from streamlit.components.v1 import html

# ─────────────────── 3.  chemins & assets ─────────────────────────────
ASSETS        = ROOT / "app/static/assets"
MEDIA_IMG_DIR = ASSETS / "media"
CSS_DIR       = ROOT  / "app/static/css"
    
# ─────────────────── 5.  config Streamlit & CSS ───────────────────────
st.set_page_config(page_title="CCF – Database",
                   page_icon="🌎",
                   layout="centered",
                   initial_sidebar_state="collapsed")
navbar(active="Database")
hide_sidebar()

for css in ("home.css", "database.css",):          # virgule = tuple d’un seul élément
    css_path = CSS_DIR / css
    if css_path.exists():
        st.markdown(f"<style>{css_path.read_text()}</style>", unsafe_allow_html=True)
    else:
        st.warning(f"CSS file not found: {css_path}")


# ─────────────────── 6.  constantes ──────────────────────────────────
AXES_WAIT, MEDIA_MS, TIME_MS = 400, 200, 3000
TITLE_WORDS = ["The", "CCF", "Database"]
BASE, STEP  = 0.30, 0.06         # animation pas-à-pas

# ─────────────────── 7.  init session state ───────────────────────────
if "view" not in st.session_state:
    st.session_state.view = None          # première visite
view = st.session_state.view

# ────────────────────────  banner of logos  ──────────────────────────
def build_logo_banner() -> str:
    """Return HTML for a looping banner of all media logos."""
    imgs_html: list[str] = []
    for img_path in sorted(MEDIA_IMG_DIR.iterdir()):
        if not img_path.is_file():
            continue
        b64 = base64.b64encode(img_path.read_bytes()).decode()
        ext = img_path.suffix.replace(".", "")
        imgs_html.append(
            f'<img src="data:image/{ext};base64,{b64}" alt="{img_path.stem} logo" />'
        )
    # Duplicate once → loop seamless
    track = "".join(imgs_html * 2)
    return f"""
    <div class="media-banner">
      <div class="banner-track">{track}</div>
    </div>
    """

st.markdown(build_logo_banner(), unsafe_allow_html=True)

# ────────────────────────  TITLE  +  BUTTONS  +  DESC  ───────────────
view = st.session_state.view

# — title (animated only once) ----------------------------------------
if view is None:        # première visite ⇒ animé
    title_html = "".join(
        f'<span class="type-word" style="animation-delay:{BASE+i*STEP:.2f}s">{w}&nbsp;</span>'
        for i, w in enumerate(TITLE_WORDS)
    )
else:
    title_html = " ".join(TITLE_WORDS)

st.markdown(f'<h1 class="db-title">{title_html}</h1>', unsafe_allow_html=True)

# — buttons (centre + no reload) -------------------------------------
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    c1, c2 = st.columns(2, gap="large")
    if c1.button("Show data by media"):
        st.session_state.view = "media"
        view = "media"
    if c2.button("Show articles over time"):
        st.session_state.view = "time"
        view = "time"

# — description text --------------------------------------------------
INTRO = {
    None: ("We exhaustively collected more than 250 000 news articles since 1978 "
           "from 20 major Canadian newspapers, extracting full texts and metadata. "
           "Explore the outlets and their article volume over time."),
    "media": ("We collected climate‑change articles from 20 outlets representative "
              "of the Canadian media landscape and with the largest readership. "
              "Below they are ordered by article count."),
    "time": ("We gathered articles reaching as far back as possible to build a corpus "
             "that is both geographically and historically exhaustive across Canada."),
}[view]

delay0 = BASE + 0.40 if view is None else 0.10
desc_html = "".join(
    f'<span class="type-word" style="animation-delay:{delay0+i*STEP:.2f}s">'
    f'{esc.escape(w)}&nbsp;</span>'
    for i, w in enumerate(INTRO.split())
)
desc_cls = "db-description alt" if view else "db-description"
st.markdown(f'<p class="{desc_cls}">{desc_html}</p>', unsafe_allow_html=True)

# ────────────────────────  DATA & CHART  ─────────────────────────────
media_df = pd.read_csv(ASSETS / "articles_by_media.csv")
month_df = (
    pd.read_csv(ASSETS / "articles_by_month.csv")
      .dropna(subset=["year", "month"])
      # ①  on force year → int  (passe de 1978.0 → 1978)
      .assign(year=lambda d: d["year"].astype(int),
              month=lambda d: d["month"].astype(int))
      # ②  on crée l’objet AAAA‑MM puis on ordonne
      .assign(year_month=lambda d:
              pd.to_datetime(d["year"].astype(str) + "-" +
                             d["month"].astype(str).str.zfill(2)))
      .sort_values("year_month")
)


if view:
    st.markdown(
        f"<h2 class='db-chart-title'>"
        f"{'Articles by Media' if view=='media' else 'Articles per Month'}</h2>",
        unsafe_allow_html=True,
    )

    if view == "media":
        labs = media_df.media.tolist()
        vals = media_df.n_articles.tolist()
        option = f"""{{
          tooltip:{{trigger:'axis'}},
          xAxis:{{type:'category',data:{json.dumps(labs)},axisLabel:{{rotate:35}}}},
          yAxis:{{type:'value',name:'Articles'}},
          series:[{{type:'bar',data:{json.dumps(vals)},
            itemStyle:{{color:{{type:'linear',x:0,y:0,x2:0,y2:1,
              colorStops:[{{offset:0,color:'#f0f1f2'}},
                          {{offset:1,color:'#41626a'}}]}}}},
            animationDelay:(i)=>{AXES_WAIT}+{MEDIA_MS}*i,
            animationDuration:{MEDIA_MS}}}]
        }}"""
    else:
        labs = month_df.year_month.dt.strftime("%Y‑%m").tolist()
        vals = month_df.n_articles.tolist()
        option = f"""{{
          tooltip:{{trigger:'axis'}},
          xAxis:{{type:'category',data:{json.dumps(labs)}}},
          yAxis:{{type:'value',name:'Articles'}},
          series:[{{type:'line',data:{json.dumps(vals)},smooth:true,symbol:'circle',
            lineStyle:{{width:3,color:'#41626a'}},
            areaStyle:{{color:'rgba(65,98,106,0.15)'}},
            animationDelay:(i)=>{AXES_WAIT}+{TIME_MS}*i,
            animationDuration:{TIME_MS}}}]
        }}"""

    html(
        f"""
<div id="eplot" style="width:100%;max-width:900px;height:520px;margin:auto"></div>
<script src="https://cdn.jsdelivr.net/npm/echarts@5/dist/echarts.min.js"></script>
<script>
const chart = echarts.init(document.getElementById('eplot'), null, {{renderer:'svg'}});
chart.setOption({option});
window.addEventListener('resize', () => chart.resize());
</script>
""",
        height=560,
    )
