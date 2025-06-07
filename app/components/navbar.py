"""
Navigation bar component  – sticky version
==========================================

• Boutons = classe `.cta-btn` déjà définie dans *home.css*
• Injecte *home.css* automatiquement (sauf sur la page Home)
• Logo translucide centré derrière la barre
• Barre fixe en haut quand on scrolle (position:sticky)

Usage
-----
    from app.components.navbar import navbar
    navbar(active="Database")
"""
from pathlib import Path
import base64
import streamlit as st

# ------------------------------------------------------------------ #
# 1 . Pages                                                          #
# ------------------------------------------------------------------ #
LINKS = {
    "Home":     "/Home",
    "Database": "/Database",
    "Idea":     "/Idea",
    "Analysis": "/Analysis",
}

# ------------------------------------------------------------------ #
# 2 . Helpers                                                         #
# ------------------------------------------------------------------ #
ROOT = Path(__file__).resolve().parents[2]


def _inject_home_css() -> None:
    """Inject *home.css* une seule fois (nécessaire pour .cta-btn)."""
    css_path = ROOT / "app/static/css/home.css"
    if css_path.exists() and "ccf-home-css" not in st.session_state:
        st.session_state["ccf-home-css"] = True
        st.markdown(
            f"<style id='ccf-home-css'>{css_path.read_text()}</style>",
            unsafe_allow_html=True,
        )


def _logo_b64() -> str | None:
    path = ROOT / "app/static/assets/CCF_icone.png"
    return None if not path.exists() else base64.b64encode(path.read_bytes()).decode()


# ------------------------------------------------------------------ #
# 3 . Composant principal                                             #
# ------------------------------------------------------------------ #
def navbar(active: str = "Home") -> None:
    """Affiche la barre de navigation (cachée sur la page Home)."""
    if active.lower() == "home":
        return

    _inject_home_css()

    # ——— logo translucide ———
    logo = _logo_b64()
    logo_html = (
        f'<img src="data:image/png;base64,{logo}" class="navbar-logo" alt="CCF logo" />'
        if logo else ""
    )

    # ——— CSS ———
    st.markdown(
        f"""
<style>
/* wrapper sticky + fond flouté léger ----------------------------- */
.navbar-wrapper {{
    position:sticky;           /* reste collé en haut */
    top:0;                     /* point d’ancrage     */
    z-index:100;               /* au-dessus du reste  */
    backdrop-filter:blur(4px); /* glassy             */
    margin:0;                  /* annule les marges  */
    padding:.6rem 0;           /* espace intérieur   */
}}

/* contenu flex --------------------------------------------------- */
.navbar {{
    display:flex; flex-wrap:wrap; gap:1rem;
    justify-content:center;
    padding:0 .5rem;
}}

/* bouton actif légèrement atténué ------------------------------- */
.navbar .active {{ filter:brightness(.85); }}

/* logo translucide centré --------------------------------------- */
.navbar-logo {{
    position:absolute; inset:0; margin:auto;
    width:110px; max-width:30vw;
    opacity:.15; pointer-events:none; user-select:none;
}}

/* mobile tweaks -------------------------------------------------- */
@media (max-width:500px) {{
  .navbar {{ gap:.6rem }}
  .navbar .cta-btn {{ padding:.55rem 1rem; font-size:.9rem }}
}}

/* évite que le contenu passe sous la barre ---------------------- */
[data-testid="stAppViewContainer"] > div:first-child {{
    padding-top:3.6rem;        /* ≈ hauteur barre */
}}
</style>
""",
        unsafe_allow_html=True,
    )

    # ——— HTML des liens ———
    links_html = "".join(
        f'<a class="cta-btn {"active" if name==active else ""}" '
        f'href="{url}" target="_self">{name}</a>'
        for name, url in LINKS.items()
    )

    st.markdown(
        f"""
<div class="navbar-wrapper">
    {logo_html}
    <nav class="navbar">
        {links_html}
    </nav>
</div>
""",
        unsafe_allow_html=True,
    )
