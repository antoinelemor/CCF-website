"""
Database page
─────────────
1) Animated title (first load only) + intro
2) Two centred "glass" buttons (no page reload)
3) Click => show ECharts chart in-place
"""

from __future__ import annotations
import sys, json, html as esc
from pathlib import Path
import pandas as pd
import streamlit as st
from streamlit.components.v1 import html
from app.components.navbar import navbar
ROOT = Path(__file__).resolve().parents[2]   # dossier racine du projet
if str(ROOT) not in sys.path:                # ← ajoute-le au PYTHONPATH
    sys.path.insert(0, str(ROOT))
from app.components.ui_utils import hide_sidebar

# ─────────────────────────  CONSTANTS  ─────────────────────────
AXES_WAIT, MEDIA_MS, TIME_MS = 400, 200, 3000   # ECharts animation delays
TITLE_WORDS = ["The", "CCF", "Database"]     # for the animated title
BASE, STEP = 0.30, 0.06                     # word-by-word delay for title+desc

# ──────────────────────  BOILERPLATE SETUP  ────────────────────

st.set_page_config(
    page_title="CCF – Database",
    page_icon="🌎",
    layout="centered",
    initial_sidebar_state="collapsed",
)
navbar(active="Database")
hide_sidebar()

# Load custom CSS
for css_file in ("home.css", "database.css"):
    st.markdown(
        f"<style>{(ROOT / 'app' / 'static' / 'css' / css_file).read_text()}</style>",
        unsafe_allow_html=True
    )

# ─────────────────────────  STATE INIT  ────────────────────────
# If "view" is not in session state, it's first load => animate the title.
if "view" not in st.session_state:
    st.session_state["view"] = None

# ─────────────────────  BUTTONS (NO PAGE RELOAD)  ──────────────
# Display two centered "glass" buttons. Clicking sets st.session_state["view"].

# Container for centering them
btn_container = st.container()
with btn_container:
    spacer, main_col, spacer2 = st.columns([1, 2, 1])
    with main_col:
        c1, c2 = st.columns([1, 1], gap="large")  # equal-width columns
        with c1:
            btn_media = st.button("Show data by media", key="btn_media")
        with c2:
            btn_time = st.button("Show articles over time", key="btn_time")

# Process button clicks (no page reload, but the script re-runs)
if btn_media:
    st.session_state["view"] = "media"
elif btn_time:
    st.session_state["view"] = "time"

view = st.session_state["view"]  # read the updated state

# ─────────────────────  TEXTS / INTRO  ─────────────────────────
# The descriptive text depends on the active view (None, "media", or "time").
INTRO_DICT = {
    None: (
        "We exhaustively collected more than 250 000 news articles since 1978 "
        "from 20 major Canadian newspapers, extracting full texts and metadata. "
        "Below you can explore the database structure – the outlets and how "
        "article volume evolves over time. Enjoy!"
    ),
    "media": (
        "We collected climate-change articles from 20 outlets representative of "
        "the Canadian media landscape with the largest readership. The number of articles per media are "
        "displayed below in descending order of article count."
    ),
    "time": (
        "We gathered articles reaching as far back as "
        "possible to build an historically exhaustive corpus of climate-change articles "
        "for Canada."
    ),
}
intro_text = INTRO_DICT[view]

# ─────────────────────  HERO (TITLE + DESCRIPTION)  ────────────
# 1) Title: animate if view=None (first page load), else static.
if view is None:
    # Animated title
    title_html = "".join(
        f'<span class="type-word" style="animation-delay:{BASE + i*STEP:.2f}s">'
        f"{word}&nbsp;</span>"
        for i, word in enumerate(TITLE_WORDS)
    )
else:
    # Static title (user has clicked a button)
    title_html = " ".join(TITLE_WORDS)

# 2) Description: always word-by-word. If view is None => slower start.
desc_delay = BASE + 0.4 if view is None else 0.10
desc_html = "".join(
    f'<span class="type-word" style="animation-delay:{desc_delay + i*STEP:.2f}s">'
    f"{esc.escape(word)}&nbsp;</span>"
    for i, word in enumerate(intro_text.split())
)

# Light-grey & italic style if "media" or "time" (see .db-description.alt)
desc_class = "db-description alt" if view else "db-description"

st.markdown(
    f"""
<section class="db-hero">
  <h1 class="db-title">{title_html}</h1>
  <p class="{desc_class}">{desc_html}</p>
</section>
""",
    unsafe_allow_html=True,
)

# ─────────────────────  LOAD DATA & SHOW CHART  ────────────────
ASSETS = ROOT / "app" / "static" / "assets"
media_df = pd.read_csv(ASSETS / "articles_by_media.csv")
month_df = (
    pd.read_csv(ASSETS / "articles_by_month.csv")
    .dropna(subset=["year", "month"])
    .assign(
        year_month=lambda df: pd.to_datetime(
            df["year"].astype(int).astype(str) + "-"
            + df["month"].astype(int).astype(str).str.zfill(2)
        )
    )
    .sort_values("year_month")
)

if view:
    # Chart title
    if view == "media":
        chart_title = "Articles by Media"
    else:
        chart_title = "Articles per Month"

    st.markdown(f"<h2 class='db-chart-title'>{chart_title}</h2>", unsafe_allow_html=True)

    # Build ECharts option
    if view == "media":
        labels = media_df["media"].tolist()
        values = media_df["n_articles"].tolist()
        echarts_option = f"""{{
          tooltip:{{trigger:'axis'}},
          xAxis:{{type:'category',data:{json.dumps(labels)},axisLabel:{{rotate:35}}}},
          yAxis:{{type:'value',name:'Articles'}},
          series:[{{
            type:'bar',
            data:{json.dumps(values)},
            itemStyle:{{color:{{type:'linear',x:0,y:0,x2:0,y2:1,
              colorStops:[
                {{offset:0,color:'#f0f1f2'}},
                {{offset:1,color:'#41626a'}}
              ]
            }}}},
            animationDelay:(i)=>{AXES_WAIT}+{MEDIA_MS}*i,
            animationDuration:{MEDIA_MS}
          }}]
        }}"""
    else:
        labels = month_df["year_month"].dt.strftime("%Y-%m").tolist()
        values = month_df["n_articles"].tolist()
        echarts_option = f"""{{
          tooltip:{{trigger:'axis'}},
          xAxis:{{type:'category',data:{json.dumps(labels)}}},
          yAxis:{{type:'value',name:'Articles'}},
          series:[{{
            type:'line',
            data:{json.dumps(values)},
            smooth:true,
            symbol:'circle',
            lineStyle:{{width:3,color:'#41626a'}},
            areaStyle:{{color:'rgba(65,98,106,0.15)'}},
            animationDelay:(i)=>{AXES_WAIT}+{TIME_MS}*i,
            animationDuration:{TIME_MS}
          }}]
        }}"""

    # Render ECharts in-place
    html(
        f"""
        <div id="eplot" style="width:100%;max-width:900px;height:520px;margin:auto"></div>
        <script src="https://cdn.jsdelivr.net/npm/echarts@5/dist/echarts.min.js"></script>
        <script>
          const chart = echarts.init(document.getElementById('eplot'), null, {{renderer:'svg'}});
          chart.setOption({echarts_option});
          window.addEventListener('resize', () => chart.resize());
        </script>
        """,
        height=560
    )
