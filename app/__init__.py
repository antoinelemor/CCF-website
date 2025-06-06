"""
app package
-----------
Ne contient plus d’import direct sur navbar : tout est
re-exporté proprement par app.components.
"""

# expose seulement les sous-packages utiles
from importlib import import_module

# Charge dynamiquement app.components pour éviter les import loops
import_module("app.components")

__all__: list[str] = ["components"]
