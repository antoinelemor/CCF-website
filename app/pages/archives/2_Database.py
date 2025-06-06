"""
2_Database.py – Animated corpus explorer (auto-play, timing knobs)
------------------------------------------------------------------
Modifier MEDIA_MS ou TIME_MS pour ralentir / accélérer l’animation.

MEDIA_MS : durée (ms) entre deux barres de l’histogramme
TIME_MS  : durée (ms) entre deux points de la courbe
"""

from __future__ import annotations
import sys
from pathlib import Path
import pandas as pd
import plotly.graph_objects as go
import plotly.io as pio
import streamlit as st
from streamlit.components.v1 import html

# ╔════════════ Réglages vitesse (ms par frame) ════════════════════╗
MEDIA_MS = 90     # histogramme (articles par média)
TIME_MS  = 1     # courbe (articles par mois)
# ╚═════════════════════════════════════════════════════════════════╝

# ─────────────────────────── install context ──────────────────────
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

# ─────────────────────────── charge les CSV ───────────────────────
ASSETS = ROOT / "app" / "static" / "assets"
media_df = pd.read_csv(ASSETS / "articles_by_media.csv")

month_df = pd.read_csv(ASSETS / "articles_by_month.csv").dropna(subset=["year", "month"])
month_df["year_month"] = pd.to_datetime(
    month_df["year"].astype(int).astype(str) + "-" +
    month_df["month"].astype(int).astype(str).str.zfill(2),
    format="%Y-%m"
)

# ───────────────────────── utilitaires Plotly ─────────────────────
def frames_bars(x, y):
    return [
        go.Frame(data=[go.Bar(x=x, y=y[:i])])
        for i in range(1, len(y) + 1)
    ]

def frames_line(x, y):
    return [
        go.Frame(data=[go.Scatter(x=x[:i], y=y[:i], mode="lines")])
        for i in range(1, len(y) + 1)
    ]

def layout_common(title: str, frame_ms: int):
    """Layout + bouton Play invisible ; duration réglé."""
    return dict(
        title=title,
        template="plotly_white",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#000"),
        margin=dict(t=60, r=30, b=60, l=60),
        showlegend=False,
        updatemenus=[dict(
            type="buttons",
            visible=False,
            buttons=[dict(
                label="Play",
                method="animate",
                args=[None, {"frame": {"duration": frame_ms, "redraw": True},
                             "transition": {"duration": 0},
                             "mode": "immediate"}],
            )],
        )],
    )

def auto_play(fig: go.Figure, height=500):
    """Affiche la figure avec animation qui démarre toute seule."""
    html_str = pio.to_html(
        fig,
        include_plotlyjs="cdn",
        full_html=False,
        config={"displayModeBar": False},
        auto_play=True,
    )
    html(html_str, height=height, width=None)

# ─────────────────────────── boutons UI ────────────────────────────
col1, col2 = st.columns(2)
view = st.session_state.get("view", "media")
if col1.button("Show data by media"):
    view = st.session_state["view"] = "media"
if col2.button("Show articles over time"):
    view = st.session_state["view"] = "time"
st.markdown("---")

# ─────────────────────────── vue MEDIA ─────────────────────────────
if view == "media":
    st.subheader("Articles by Media")
    x, y = media_df["media"], media_df["n_articles"]

    # trace de base : toutes les barres avec hauteur 0 (axes complets)
    base = go.Bar(x=x, y=[0] * len(y), marker_line_width=0)
    fig = go.Figure(
        data=[base],
        layout=layout_common("", MEDIA_MS),
        frames=frames_bars(x, y),
    )
    fig.update_yaxes(range=[0, y.max() * 1.05], title="Articles")
    auto_play(fig)

# ─────────────────────────── vue TEMPS ─────────────────────────────
else:
    st.subheader("Articles per Month")
    df = month_df.sort_values("year_month")
    x, y = df["year_month"], df["n_articles"]

    base = go.Scatter(x=[x.min(), x.max()], y=[0, 0], mode="lines")
    fig = go.Figure(
        data=[base],
        layout=layout_common("", TIME_MS),
        frames=frames_line(x, y),
    )
    fig.update_xaxes(title="Date", tickformat="%Y-%m")
    fig.update_yaxes(range=[0, y.max() * 1.05], title="Articles")
    auto_play(fig)
