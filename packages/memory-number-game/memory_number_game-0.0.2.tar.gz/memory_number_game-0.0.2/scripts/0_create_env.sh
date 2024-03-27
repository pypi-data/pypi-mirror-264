if [ -d ".venv" ]; then rm -Rf .venv; fi
python3 -m venv .venv
source .venv/bin/activate
pip install -e .