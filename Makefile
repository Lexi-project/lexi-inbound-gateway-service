compile:
	python -m pip install --upgrade pip
	pip install pip-tools
	pip-compile requirements/requirements.in --output-file=requirements/requirements.txt

install: compile
	pip install --no-cache-dir -r requirements/requirements.txt
	rm requirements/requirements.txt

start:
	uvicorn app:app --reload --host 0.0.0.0 --port 8001