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

# ─────────────────────────  CONSTANTS  ─────────────────────────
AXES_WAIT, MEDIA_MS, TIME_MS = 400, 90, 60   # chart animation delays
TITLE_WORDS = ["The", "CCF", "Database"]     # for the animated title
BASE, STEP = 0.30, 0.06                     # word-by-word delay

# ──────────────────────  BOILERPLATE SETUP  ────────────────────
ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

st.set_page_config(
    page_title="CCF – Database",
    page_icon="🌎",
    layout="centered",
    initial_sidebar_state="collapsed",
)
navbar(active="Database")

# Load custom CSS
for css_file in ("home.css", "database.css"):
    st.markdown(
        f"<style>{(ROOT / 'app' / 'static' / 'css' / css_file).read_text()}</style>",
        unsafe_allow_html=True
    )

# ─────────────────────────  STATE  ─────────────────────────────
# If "view" is not in session state, it's first load => animate title
if "view" not in st.session_state:
    st.session_state["view"] = None

view = st.session_state["view"]  # shorthand

# ────────────────────────  TEXTS / INTRO  ──────────────────────
INTRO = {
    None: (
        "We exhaustively collected more than 250 000 news articles since 1978 "
        "from 20 major Canadian newspapers, extracting full texts and metadata. "
        "Below you can explore the database structure – the outlets and how "
        "article volume evolves over time. Enjoy!"
    ),
    "media": (
        "We collected climate-change articles from 20 outlets representative of "
        "the Canadian media landscape and with the largest readership. They are "
        "displayed below in descending order of article count."
    ),
    "time": (
        "We gathered articles from 20 leading outlets, reaching as far back as "
        "possible to build a geographically and historically exhaustive corpus "
        "for Canada."
    ),
}[view]

# ─────────────────────  HERO (title + desc)  ───────────────────
# Animate the title only if view is None (i.e. first page load)
if view is None:
    title_html = "".join(
        f'<span class="type-word" style="animation-delay:{BASE + i*STEP:.2f}s">'
        f'{word}&nbsp;</span>'
        for i, word in enumerate(TITLE_WORDS)
    )
else:
    # If user already clicked a button, show a static title
    title_html = " ".join(TITLE_WORDS)

# Description is always word-by-word, but starts faster if not first load
desc_delay = BASE + 0.4 if view is None else 0.10
desc_html = "".join(
    f'<span class="type-word" style="animation-delay:{desc_delay + i*STEP:.2f}s">'
    f'{esc.escape(w)}&nbsp;</span>'
    for i, w in enumerate(INTRO.split())
)
desc_cls = "db-description alt" if view else "db-description"

st.markdown(
    f"""
<section class="db-hero">
  <h1 class="db-title">{title_html}</h1>
  <p class="{desc_cls}">{desc_html}</p>
</section>
""",
    unsafe_allow_html=True,
)

# ─────────────────────  BUTTONS (NO RELOAD)  ──────────────────
# We'll display two centered buttons. Clicking them sets
# session_state["view"] = "media" or "time" without reloading the page.

# Container to center them via HTML or columns
btn_container = st.container()
with btn_container:
    # Use columns to center them horizontally.
    # (We avoid the ratio that triggered errors; we use numeric ratios.)
    spacer_col, main_col, spacer_col2 = st.columns([1, 2, 1])
    with main_col:
        # Put the two buttons side by side in one row:
        c1, c2 = st.columns(2, gap="large")
        with c1:
            btn_media = st.button("Show data by media", key="btn_media")
        with c2:
            btn_time = st.button("Show articles over time", key="btn_time")

# If either button is pressed, update the session state
if btn_media:
    st.session_state["view"] = "media"
    view = "media"
if btn_time:
    st.session_state["view"] = "time"
    view = "time"

# ─────────────────────  LOAD DATA / SHOW CHART  ───────────────
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
    # Show a chart title
    st.markdown(
        f"<h2 class='db-chart-title'>"
        f"{'Articles by Media' if view == 'media' else 'Articles per Month'}"
        f"</h2>",
        unsafe_allow_html=True
    )

    # Prepare the ECharts option string
    if view == "media":
        labs = media_df["media"].tolist()
        vals = media_df["n_articles"].tolist()
        option = f"""{{
          tooltip:{{trigger:'axis'}},
          xAxis:{{type:'category',data:{json.dumps(labs)},axisLabel:{{rotate:35}}}},
          yAxis:{{type:'value',name:'Articles'}},
          series:[{{
            type:'bar',
            data:{json.dumps(vals)},
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
        labs = month_df["year_month"].dt.strftime("%Y-%m").tolist()
        vals = month_df["n_articles"].tolist()
        option = f"""{{
          tooltip:{{trigger:'axis'}},
          xAxis:{{type:'category',data:{json.dumps(labs)}}},
          yAxis:{{type:'value',name:'Articles'}},
          series:[{{
            type:'line',
            data:{json.dumps(vals)},
            smooth:true,
            symbol:'circle',
            lineStyle:{{width:3,color:'#41626a'}},
            areaStyle:{{color:'rgba(65,98,106,0.15)'}},
            animationDelay:(i)=>{AXES_WAIT}+{TIME_MS}*i,
            animationDuration:{TIME_MS}
          }}]
        }}"""

    # Render ECharts in-place via HTML
    html(f"""
    <div id="eplot" style="width:100%;max-width:900px;height:520px;margin:auto"></div>
    <script src="https://cdn.jsdelivr.net/npm/echarts@5/dist/echarts.min.js"></script>
    <script>
      const chart = echarts.init(document.getElementById('eplot'), null, {{renderer:'svg'}});
      chart.setOption({option});
      window.addEventListener('resize', () => chart.resize());
    </script>
    """, height=560)
