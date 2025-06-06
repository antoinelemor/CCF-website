"""
bootstrap.py – ensure project root is in sys.path
-------------------------------------------------
Import this FIRST in every Streamlit page that lives under app/pages/.
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent      # ← dossier dépôt
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
