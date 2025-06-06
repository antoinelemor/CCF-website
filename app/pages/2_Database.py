"""
Database page
1) Animated title + intro
2) Two centred glass buttons
3) Click ⇒ animated ECharts plot *in-place*
"""
from __future__ import annotations
import json, html as esc, sys
from pathlib import Path
import pandas as pd
import streamlit as st
from streamlit.components.v1 import html

# ── timings ───────────────────────────────────────────────────────
BASE_DELAY = 300; WORD_MS = 60; MEDIA_MS = 120; TIME_MS = 4000; AXES_WAIT = 400

# ── paths & navbar ────────────────────────────────────────────────
ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path: sys.path.insert(0, str(ROOT))
from app.components import navbar                                    # noqa: E402

st.set_page_config("CCF – Database", "🌎", layout="centered",
                   initial_sidebar_state="collapsed")
navbar(active="Database")

# ── CSS (global + page) ───────────────────────────────────────────
for css_file in ("home.css", "database.css"):
    st.markdown(f"<style>{(ROOT / 'app/static/css' / css_file).read_text()}</style>",
                unsafe_allow_html=True)

# ── 1. animated title + intro ─────────────────────────────────────
TITLE_WORDS = ["The", "CCF", "Database"]
title_html = "".join(
    f'<span class="type-word" '
    f'style="animation-delay:{(BASE_DELAY+i*WORD_MS)/1000:.2f}s">{w}&nbsp;</span>'
    for i, w in enumerate(TITLE_WORDS)
)

INTRO = ("We exhaustively collected more than 250 000 news articles from "
         "20 major Canadian newspapers, extracting full texts and rich metadata. "
         "Below you can explore the database structure – the outlets and how "
         "article volume evolved over time. Enjoy!")
intro_start = BASE_DELAY + len(TITLE_WORDS)*WORD_MS + 200
intro_html = "".join(
    f'<span class="type-word" '
    f'style="animation-delay:{(intro_start+i*WORD_MS)/1000:.2f}s">'
    f'{esc.escape(w)}&nbsp;</span>'  for i, w in enumerate(INTRO.split())
)
intro_end_s = (intro_start + (len(INTRO.split())-1)*WORD_MS) / 1000

st.markdown(f"""
<section class="db-hero">
  <h1 style="font-size:clamp(2rem,3vw+1rem,2.6rem);font-weight:700;
             margin:0 0 1.2rem;text-shadow:0 1px 4px rgba(0,0,0,.35)">
    {title_html}
  </h1>
  <p class="db-description">{intro_html}</p>
</section>
""", unsafe_allow_html=True)

# ── 2. glass buttons (vrais st.button) ────────────────────────────
# ── 2. glass buttons (vrais <a>) ──────────────────────────────
fade_s = intro_end_s + .5    # délai avant apparition

st.markdown(f"""
<div class="db-btn-row" style="--btn-delay:{fade_s:.2f}s">
  <a href="?v=media" class="db-cta-btn" target="_self">
      Show&nbsp;data&nbsp;by&nbsp;media
  </a>
  <a href="?v=time"  class="db-cta-btn" target="_self">
      Show&nbsp;articles&nbsp;over&nbsp;time
  </a>
</div>
""", unsafe_allow_html=True)


# ── 3.  data & ECharts ────────────────────────────────────────────
ASSETS = ROOT / "app/static/assets"
media_df  = pd.read_csv(ASSETS / "articles_by_media.csv")
month_df  = (pd.read_csv(ASSETS / "articles_by_month.csv")
               .dropna(subset=["year","month"])
               .assign(year_month=lambda d:
                       pd.to_datetime(d.year.astype(int).astype(str)+'-'+
                                      d.month.astype(int).astype(str).str.zfill(2),
                                      format="%Y-%m"))
               .sort_values("year_month"))

q = st.query_params.get("v")
if q:
    # Streamlit ≥1.35 renvoie une str, sinon list[str]
    st.session_state.view = q if isinstance(q, str) else q[0]
    # optionnel : on nettoie l'URL pour éviter une boucle ↻
    st.query_params.clear()

# ── 3. data & ECharts ────────────────────────────────────────────
view = st.session_state.get("view")
if view:
    is_media = view == "media"
    title = "Articles by Media" if is_media else "Articles per Month"

    # Titre centré ↓
    st.markdown(
        f'<h2 class="db-chart-title">{title}</h2>',
        unsafe_allow_html=True
    )


    def echarts_option(kind: str) -> str:
        if kind == "media":
            labs = json.dumps(media_df.media.tolist())
            vals = json.dumps(media_df.n_articles.tolist())
            return f"""{{
  tooltip:{{trigger:'axis'}},
  xAxis:{{type:'category',data:{labs},axisLabel:{{rotate:35}}}},
  yAxis:{{type:'value',name:'Articles'}},
  series:[{{type:'bar',data:{vals},
    itemStyle:{{color:{{type:'linear',x:0,y:0,x2:0,y2:1,
      colorStops:[{{offset:0,color:'#f0f1f2'}},
                  {{offset:1,color:'#41626a'}}]}}}},
    animationDelay:(i)=>{AXES_WAIT}+{MEDIA_MS}*i,
    animationDuration:{MEDIA_MS}}}]
}}"""
        labs = json.dumps(month_df.year_month.dt.strftime("%Y-%m").tolist())
        vals = json.dumps(month_df.n_articles.tolist())
        return f"""{{
  tooltip:{{trigger:'axis'}},
  xAxis:{{type:'category',data:{labs}}},
  yAxis:{{type:'value',name:'Articles'}},
  series:[{{type:'line',data:{vals},smooth:true,symbol:'circle',
    lineStyle:{{width:3,color:'#41626a'}},
    areaStyle:{{color:'rgba(65,98,106,0.15)'}},
    animationDelay:(i)=>{AXES_WAIT}+{TIME_MS}*i,
    animationDuration:{TIME_MS}}}]
}}"""

    html(f"""
<div id="eplot" style="width:100%;max-width:900px;height:520px;margin:auto"></div>
<script src="https://cdn.jsdelivr.net/npm/echarts@5/dist/echarts.min.js"></script>
<script>
const chart = echarts.init(document.getElementById('eplot'), null,
                           {{renderer:'svg'}});
chart.setOption({echarts_option('media' if is_media else 'time')});
window.addEventListener('resize', ()=>chart.resize());
</script>
""", height=560)
