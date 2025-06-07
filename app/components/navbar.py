"""
Navigation bar component – sticky & centred logo
------------------------------------------------
• garde les .cta-btn de home.css
• barre fixe, translucide, logo centré
• la barre se trouve 8 px sous le haut de la fenêtre
"""
from pathlib import Path
import base64
import streamlit as st

LINKS = {
    "Home": "/Home",
    "Database": "/Database",
    "Idea": "/Idea",
    "Analysis": "/Analysis",
}

ROOT = Path(__file__).resolve().parents[2]


def _inject_home_css() -> None:
    css_path = ROOT / "app/static/css/home.css"
    if css_path.exists() and "ccf-home-css" not in st.session_state:
        st.session_state["ccf-home-css"] = True
        st.markdown(
            f"<style id='ccf-home-css'>{css_path.read_text()}</style>",
            unsafe_allow_html=True,
        )


def _logo_b64() -> str | None:
    logo_path = ROOT / "app/static/assets/CCF_icone.png"
    return (
        base64.b64encode(logo_path.read_bytes()).decode()
        if logo_path.exists()
        else None
    )


def navbar(active: str = "Home") -> None:
    if active.lower() == "home":
        return

    _inject_home_css()
    logo_b64 = _logo_b64()
    logo_html = (
        f'<img src="data:image/png;base64,{logo_b64}" '
        f'class="navbar-logo" alt="CCF logo" />'
        if logo_b64
        else ""
    )

    # Valeurs centrales (facile à régler) 🔧
    GAP_TOP = "20px"         # distance barre ↔ haut de la fenêtre
    NAV_H   = "3.1rem"      # hauteur approximative de la barre

    st.markdown(
        f"""
<style>
/* 0 — on retire complètement le header Streamlit  */
[data-testid="stHeader"] {{ display:none !important; }}

/* 1 — barre fixe, fond flouté, décalée de GAP_TOP */
.navbar-wrapper{{
    position:fixed;
    top:{GAP_TOP}; left:0; right:0;
    z-index:1000;
    backdrop-filter:blur(4px);
    padding:.55rem 0;
}}

/* 2 — flex interne */
.navbar{{
    display:flex; flex-wrap:wrap; gap:1rem;
    justify-content:center;
    padding:0 .5rem;
}}
.navbar .active{{ filter:brightness(.85); }}

/* 3 — logo translucide centré */
.navbar-logo{{
    position:absolute; inset:0; margin:auto;
    width:110px; max-width:30vw;
    opacity:.15; pointer-events:none; user-select:none;
}}

/* 4 — responsive */
@media (max-width:500px){{
  .navbar{{gap:.6rem}}
  .navbar .cta-btn{{padding:.55rem 1rem; font-size:.9rem}}
}}

/* 5 — marge haute pour ne rien masquer  */
[data-testid="stAppViewContainer"] > div:first-child{{
    padding-top:calc({NAV_H} + {GAP_TOP});
}}
</style>
""",
        unsafe_allow_html=True,
    )

    links_html = "".join(
        f'<a class="cta-btn {"active" if name==active else ""}" '
        f'href="{url}" target="_self">{name}</a>'
        for name, url in LINKS.items()
    )

    st.markdown(
        f"""
<div class="navbar-wrapper">
    {logo_html}
    <nav class="navbar">{links_html}</nav>
</div>
""",
        unsafe_allow_html=True,
    )
