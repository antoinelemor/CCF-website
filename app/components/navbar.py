"""Sticky buttons navbar visible on every page during scrolling."""

from __future__ import annotations

from typing import Iterable, Literal

import streamlit as st

PageName = Literal["Home", "Database", "Idea", "Analysis"]

NAV_STYLE = """
<style>
body{padding-top:74px;}
.sticky-nav{
    position:fixed; top:0; left:0; width:100%;
    display:flex; justify-content:center;
    z-index:3000;
    pointer-events:none;
    user-select:none;
}
.navbar{
    display:flex; gap:1rem; padding:.55rem 0;
    pointer-events:auto;
}
.nav-btn{
    display:inline-flex; align-items:center; justify-content:center; gap:.3rem;
    min-width:110px; padding:.45rem 1.2rem;
    font-weight:700; border-radius:999px; text-decoration:none;
    background:linear-gradient(135deg,#3f83ff 0%,#ffffff 100%);
    color:#0a2342 !important; box-shadow:0 2px 6px rgba(0,0,0,.18);
    transition:transform .18s, box-shadow .18s;
}
.nav-btn:hover{
    transform:translateY(-3px); box-shadow:0 4px 12px rgba(0,0,0,.28);
}
.nav-btn.active,
.nav-btn:disabled{
    pointer-events:none;
    background:linear-gradient(135deg,#184eea 0%,#c7d9ff 100%);
    color:#fff !important; box-shadow:0 3px 9px rgba(0,0,0,.25);
}
</style>
"""

PAGES: Iterable[tuple[str, str, str]] = (
    ("Home", "/Home", "🏠"),
    ("Database", "/Database", "🗄️"),
    ("Idea", "/Idea", "💡"),
    ("Analysis", "/Analysis", "📊"),
)


def navbar(active: PageName = "Home") -> None:
    """Render the sticky navigation bar."""
    st.markdown(NAV_STYLE, unsafe_allow_html=True)

    buttons = "".join(
        f'<a class="nav-btn {"active" if label==active else ""}" '
        f'href="{url}" target="_self">{icon}<span>{label}</span></a>'
        for label, url, icon in PAGES
    )
    st.markdown(
        f'<div class="sticky-nav"><nav class="navbar">{buttons}</nav></div>',
        unsafe_allow_html=True,
    )
