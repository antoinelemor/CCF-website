"""
Navigation bar component (with centred translucent logo)
========================================================
• Keeps the original “glass” CTA buttons (class **.cta-btn** from *home.css*).
• Automatically injects *home.css* on every non-Home page (safe if already loaded).
• Adds the project logo **behind** the bar (opacity ≈ 0.15, centred, no clicks).
• Bar stays hidden when `active="Home"`.

Usage
-----
    from app.components.navbar import navbar
    navbar(active="Database")
"""
from pathlib import Path
import base64
import streamlit as st


# ------------------------------------------------------------------ #
# 1 . Logical routes                                                 #
# ------------------------------------------------------------------ #
LINKS = {
    "Home":     "/Home",
    "Database": "/Database",
    "Idea":     "/Idea",
    "Analysis": "/Analysis",
}

# ------------------------------------------------------------------ #
# 2 . Helpers                                                        #
# ------------------------------------------------------------------ #
ROOT = Path(__file__).resolve().parents[2]         # project root


def _inject_home_css() -> None:
    """Load `app/static/css/home.css` once if not already present."""
    css_file = ROOT / "app" / "static" / "css" / "home.css"
    if css_file.exists() and "ccf-home-css" not in st.session_state:
        st.session_state["ccf-home-css"] = True
        st.markdown(
            f"<style id='ccf-home-css'>{css_file.read_text(encoding='utf-8')}</style>",
            unsafe_allow_html=True,
        )
    elif not css_file.exists():
        st.warning("⚠️ home.css not found – navbar style may differ.")


def _logo_base64() -> str | None:
    """Return base64 string for the logo (or *None* if missing)."""
    logo_path = ROOT / "app" / "static" / "assets" / "CCF_icone.jpg"
    if not logo_path.exists():
        return None
    return base64.b64encode(logo_path.read_bytes()).decode()


# ------------------------------------------------------------------ #
# 3 . Main entry point                                               #
# ------------------------------------------------------------------ #
def navbar(active: str = "Home") -> None:
    """Render the nav bar (hidden on the Home page)."""
    if active.lower() == "home":
        return  # keep the landing hero perfectly clean

    _inject_home_css()

    # ----------  extra CSS for the bar + logo  ----------
    logo_b64 = _logo_base64()
    logo_css = ""
    logo_html = ""
    if logo_b64:
        logo_css = """
        .navbar-wrapper{
            position:relative;
        }
        .navbar-logo{
            position:absolute;
            top:50%;left:50%;
            transform:translate(-50%,-50%);
            width:110px;               /* adjust size here */
            opacity:0.15;              /* transparency */
            pointer-events:none;
            user-select:none;
        }
        """
        logo_html = (
            f'<img src="data:image/jpg;base64,{logo_b64}" '
            f'class="navbar-logo" alt="CCF logo" />'
        )

    st.markdown(
        f"""
        <style>
        /* ----------------------------------------------- *
           NAV BAR LAYOUT (it relies on .cta-btn from home.css)
           ----------------------------------------------- */
        .navbar{{display:flex;flex-wrap:wrap;gap:1rem;
                 justify-content:center;margin:1.5rem 0 2rem;
                 padding:0 .5rem;position:relative;z-index:1;}}
        .navbar .active{{filter:brightness(0.85)}}

        /* Mobile tweaks */
        @media (max-width:500px){{
          .navbar{{gap:.6rem}}
          .navbar .cta-btn{{padding:.55rem 1rem;font-size:.9rem}}
        }}

        {logo_css}
        </style>
        """,
        unsafe_allow_html=True,
    )

    # ----------  HTML structure  ----------
    links_html = "".join(
        f'<a class="cta-btn {"active" if name == active else ""}" '
        f'href="{target}" target="_self">{name}</a>'
        for name, target in LINKS.items()
    )

    st.markdown(
        f"""
        <div class="navbar-wrapper">
            {logo_html}                <!-- centred translucent logo -->
            <nav class="navbar">{links_html}</nav>
        </div>
        """,
        unsafe_allow_html=True,
    )
