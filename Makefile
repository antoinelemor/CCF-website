.PHONY: run lint clean

run:              # lance Streamlit avec l’environnement virtuel
	. ./.venv/bin/activate && \
	PYTHONPATH=$$PWD streamlit run app/main.py   # ← ajoute la racine au path

lint:             # vérifie le style
	flake8 app

clean:            # ménage
	rm -rf __pycache__ .pytest_cache
