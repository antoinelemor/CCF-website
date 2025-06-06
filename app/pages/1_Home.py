"""
1_Home.py  – minimal, no f-string pitfalls
=========================================
* Loads external CSS (`app/static/css/home.css`).
* Inserts hero HTML where `{LOGO_URL}` placeholder is replaced at runtime.
* **No** braces inside an f-string → no more `SyntaxError`.

---
Folder checklist
----------------
app/
 ├── pages/1_Home.py   ← this file
 └── static/
      ├── css/home.css  ← provided earlier
      └── CCF_icone.jpg ← project logo

Run:
    streamlit run app/pages/1_Home.py
"""

from pathlib import Path
import streamlit as st
from streamlit.components.v1 import html

# ────────── config ──────────
st.set_page_config(page_title="CCF – Home", page_icon="🌎", layout="centered")

# ────────── locate assets ──────────
BASE = Path(__file__).resolve().parents[1]
css_file = BASE / "static" / "css" / "home.css"
logo_file = BASE / "static" / "assets" / "CCF_icone.jpg"

if not (css_file.exists() and logo_file.exists()):
    st.error(
        "Missing css or logo. Expected:\n"
        "  • app/static/css/home.css\n"
        "  • app/static/assets/CCF_icone.jpg"
    )
    st.stop()

# read CSS
css_content = css_file.read_text(encoding="utf-8")
logo_url = "/app/static/assets/CCF_icone.jpg"  # Streamlit serves this path automatically

# HTML template with placeholder
HTML = f"""
<style>{css_content}</style>
<section class="hero">
   <img src="{logo_url}" class="bg-img" />
   <h1 class="tagline">Welcome to the CCF Project</h1>
   <div class="button-row">
      <a href="?page=database"  class="cta-btn">The Database</a>
      <a href="?page=idea"      class="cta-btn">Project Idea</a>
      <a href="?page=analysis"  class="cta-btn">Some Analysis</a>
   </div>
</section>
"""

html(HTML, height=0, scrolling=False)

# ────────── optionally show below-hero section ──────────
page = st.query_params.get("page", "home")

if page == "database":
    st.header("The Database")
    st.write("Describe corpus size, media sources, access policy …")
elif page == "idea":
    st.header("Project Idea")
    st.write("Explain research questions, theoretical framework, objectives …")
elif page == "analysis":
    st.header("Some Analysis")
    st.write("Teaser charts or metrics coming soon …")