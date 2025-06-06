"""
2_Database.py – ECharts explorer (axes-first, hover, vitesse réglable)
---------------------------------------------------------------------
* Histogramme : barres gradient qui montent l’une après l’autre.
* Courbe : trait lissé qui se dessine point par point.
"""

from __future__ import annotations
import sys, json
from pathlib import Path
import pandas as pd
import streamlit as st
from streamlit.components.v1 import html

# ╔══════════  paramétrage vitesse (ms) ═════════╗
MEDIA_MS  = 90      # durée d’apparition d’UNE barre
TIME_MS   = 4000      # durée d’apparition d’UN point
AXES_WAIT = 400     # délai après axes avant démarrage série
# ╚══════════════════════════════════════════════╝

# ── bootstrap page ────────────────────────────────────────────────
ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from app.components import navbar  # noqa: E402

st.set_page_config("CCF – Database", "🌎", layout="centered",
                   initial_sidebar_state="collapsed")
navbar(active="Database")

CSS = (ROOT / "app" / "static" / "css" / "database.css").read_text()
st.markdown(f"<style>{CSS}</style>", unsafe_allow_html=True)
st.title("Explore the Corpus")

# ── load data ─────────────────────────────────────────────────────
ASSETS   = ROOT / "app" / "static" / "assets"
media_df = pd.read_csv(ASSETS / "articles_by_media.csv")

month_df = pd.read_csv(ASSETS / "articles_by_month.csv").dropna(subset=["year", "month"])
month_df["year_month"] = pd.to_datetime(
    month_df["year"].astype(int).astype(str) + "-" +
    month_df["month"].astype(int).astype(str).str.zfill(2),
    format="%Y-%m"
).sort_values()

# ── Streamlit view selector ───────────────────────────────────────
col1, col2 = st.columns(2)
view = st.session_state.get("view", "media")
if col1.button("Show data by media"):
    view = st.session_state["view"] = "media"
if col2.button("Show articles over time"):
    view = st.session_state["view"] = "time"
st.markdown("---")

# ╭──────────────────────── helper : construit l’option JS ─────────╮
def build_option_js(kind: str) -> str:
    """Retourne une chaîne JS représentant l'objet option ECharts."""
    if kind == "media":
        labels = json.dumps(media_df["media"].tolist())
        values = json.dumps(media_df["n_articles"].tolist())
        return f"""
{{
  backgroundColor:'rgba(0,0,0,0)',
  tooltip:{{trigger:'axis'}},
  xAxis:{{type:'category',data:{labels},axisLabel:{{rotate:35}}}},
  yAxis:{{type:'value',name:'Articles'}},
  series:[{{
    type:'bar',
    data:{values},
    itemStyle:{{
      color:{{
        type:'linear',x:0,y:0,x2:0,y2:1,
        colorStops:[
          {{offset:0,color:'#f0f1f2'}},
          {{offset:1,color:'#41626a'}}
        ]
      }}
    }},
    animationDelay:(idx)=>{AXES_WAIT}+{MEDIA_MS}*idx,
    animationDuration:{MEDIA_MS},
    animationEasing:'cubicOut',
    emphasis:{{scale:true,itemStyle:{{color:'#ffaf6e'}}}}
  }}]
}}"""
    # --- time series -------------------------------------------------
    labels = json.dumps(month_df["year_month"].dt.strftime("%Y-%m").tolist())
    values = json.dumps(month_df["n_articles"].tolist())
    return f"""
{{
  backgroundColor:'rgba(0,0,0,0)',
  tooltip:{{trigger:'axis'}},
  xAxis:{{type:'category',data:{labels}}},
  yAxis:{{type:'value',name:'Articles'}},
  series:[{{
    type:'line',
    data:{values},
    smooth:true,
    lineStyle:{{width:3,color:'#41626a'}},
    areaStyle:{{color:'rgba(65,98,106,0.15)'}},
    animationDelay:(idx)=>{AXES_WAIT}+{TIME_MS}*idx,
    animationDuration:{TIME_MS},
    animationEasing:'linear'
  }}]
}}"""

# ╭───────────────────────── render HTML component ─────────────────╮
ECHARTS_CDN = "https://cdn.jsdelivr.net/npm/echarts@5/dist/echarts.min.js"
chart_id    = "echarts_div"

opt_js = build_option_js("media" if view == "media" else "time")
subtitle = "Articles by Media" if view == "media" else "Articles per Month"
st.subheader(subtitle)

html(f"""
<div id="{chart_id}" style="width:100%;height:520px;"></div>
<script src="{ECHARTS_CDN}"></script>
<script>
(function(){{
  const chart = echarts.init(document.getElementById('{chart_id}'), null, {{renderer:'svg'}});
  chart.setOption({opt_js});
  window.addEventListener('resize', ()=>chart.resize());
}})();
</script>
""", height=540, width=None)
