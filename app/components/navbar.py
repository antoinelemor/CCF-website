"""
Navigation bar component
========================
• Re-uses the `.cta-btn` class defined in *home.css* so the buttons look
  **identical** to the hero CTA buttons.
• Loads *home.css* automatically on every non-Home page (safe if already
  loaded).
• Hidden when `active="Home"`.

Usage
-----
    from app.components.navbar import navbar
    navbar(active="Database")
"""
from pathlib import Path
import streamlit as st

# Logical routes --------------------------------------------------------------
LINKS = {
    "Home":     "/Home",
    "Database": "/Database",
    "Idea":     "/Idea",
    "Analysis": "/Analysis",
}

# -----------------------------------------------------------------------------


def _inject_home_css() -> None:
    """Load `app/static/css/home.css` once, if not already present."""
    root = Path(__file__).resolve().parents[2]          # project root
    css_file = root / "app" / "static" / "css" / "home.css"

    if css_file.exists():
        css_content = css_file.read_text(encoding="utf-8")
        # Add an ID so we don’t inject twice on re-runs
        st.markdown(
            f"<style id='ccf-home-css'>{css_content}</style>",
            unsafe_allow_html=True,
        )
    else:
        st.warning("⚠️ home.css not found – navbar style may differ.")


def navbar(active: str = "Home") -> None:
    """Render the nav bar unless we are on the landing page.

    Parameters
    ----------
    active : str, optional
        Logical name of the current page (case-insensitive).
    """
    if active.lower() == "home":
        return  # keep the hero page clean

    _inject_home_css()  # ensures .cta-btn is available everywhere

    # Extra layout styles specific to the nav container
    st.markdown(
        """
        <style>
        .navbar{
            display:flex;
            gap:1rem;
            justify-content:center;
            margin:1.5rem 0 2rem;
        }
        /* Highlight current page */
        .navbar .active{
            filter:brightness(0.85);
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    links_html = "".join(
        f'<a class="cta-btn {"active" if name == active else ""}" '
        f'href="{target}" target="_self">{name}</a>'
        for name, target in LINKS.items()
    )
    st.markdown(f'<nav class="navbar">{links_html}</nav>', unsafe_allow_html=True)
