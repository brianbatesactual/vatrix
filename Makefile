# --------- CONFIG ---------
VENV_DIR := env
PYTHON := $(VENV_DIR)/bin/python
PIP := $(VENV_DIR)/bin/pip
LOG_LEVEL ?= INFO
LOG_FILE ?=
RENDER_MODE ?= random
INPUT ?= sample_logs/input_logs.ndjson
OUTPUT ?=
UNMATCHED ?=
SBERT_OUT ?=

# --------- COMMANDS ---------
.PHONY: help setup run stream test clean freeze retrain

help:
	@echo ""
	@echo "Makefile for vatrix"
	@echo "Usage:"
	@echo "  make setup        Create virtualenv & install requirements"
	@echo "  make run          Run the pipeline with default file input"
	@echo "  make stream       Start streaming input from stdin"
	@echo "  make test         Run SBERT test"
	@echo "  make freeze       Regenerate requirements.txt"
	@echo "  make retrain      Generate SBERT training pairs"
	@echo "  make clean        Delete env and temp data files"
	@echo ""

setup:
	python3 -m venv $(VENV_DIR)
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt

run:
	PYTHONPATH=src $(PYTHON) -m src.vatrix.main \
		--mode file \
		--render-mode all \
		--log-level $(LOG_LEVEL) \
		$(if $(LOG_FILE),--log-file $(LOG_FILE),)

stream:
	PYTHONPATH=src $(PYTHON) -m src.vatrix.main \
		--mode stream \
		--render-mode $(RENDER_MODE) \
		--log-level $(LOG_LEVEL) \
		$(if $(LOG_FILE),--log-file $(LOG_FILE),)

train:
	PYTHONPATH=src $(PYTHON) -m src.vatrix.main \
		--mode file \
		--render-mode all \
		--generate-sbert-data \
		--input $(INPUT) \
		$(if $(SBERT_OUT),--output $(SBERT_OUT),) \
		--unmatched $(UNMATCHED) \
		--log-level $(LOG_LEVEL)

test-model:
	$(PYTHON) -c "from sentence_transformers import SentenceTransformer; m = SentenceTransformer('all-MiniLM-L6-v2'); print(m.encode('hello')[:5])"

freeze:
	$(PIP) freeze > requirements.txt

similarity:
	@read -p "Sentence 1: " s1; \
	read -p "Sentence 2: " s2; \
	PYTHONPATH=src $(PYTHON) -c "from vatrix.utils.similarity import get_similarity_score; print(f'Score: {get_similarity_score(\"$$s1\", \"$$s2\")}')"

# ---------- Testing Utilities ----------
test:
	pytest src/vatrix/tests/ -v

test-paths:
	python src/vatrix/tests/test_pathing.py

test-stream:
	python src/vatrix/tests/test_rotating_writer.py

test-e2e:
	python src/vatrix/tests/test_pipeline_end_to_end.py

validate: test test-paths test-stream test-e2e
	@echo "##### All tests passed. System validated! #####"

stream-debug:
	make stream LOG_LEVEL=debug

run-debug:
	make run LOG_LEVEL=debug

retrain-debug:
	make retrain LOG_LEVEL=debug

tail:
	@echo "📜 Tailing latest log file..."
	tail -f logs/$$(ls -t logs/* | head -n 1)

renew:
	rm -rf *.egg-info
	python3 -m build
	pip install -e .

clean:
	rm -rf env data/*.csv data/*.json __pycache__ src/**/__pycache__ .pytest_cache
	rm -rf *.egg-info build dist

# ---------- Build Utilities ----------
test-release:
	@echo "🧹 Cleaning old distributions..."
	rm -rf dist
	@echo "🚀 Building distribution..."
	python3 -m build
	@echo "🔐 Uploading to TestPyPI..."
	twine upload --repository testpypi dist/* --verbose
	@echo "✅ Test release published to https://test.pypi.org/project/vatrix/"

release:
	@echo "🧹 Cleaning old distributions..."
	rm -rf dist
	@echo "🚀 Building distribution..."
	python3 -m build
	@echo "🔐 Uploading to PyPI..."
	twine upload dist/* --verbose
	@echo "✅ Release published to https://pypi.org/project/vatrix/"

# ---------- Nuke 'em Rico ----------
nuke:
	@set -e; \
	read -p "🚨 Are you sure you want to nuke? (y/n)" yn; \
	if [ $$yn = "y" ]; then \
		echo "💥 Nuking environment and project data..."; \
		rm -rf env data/*.csv data/*.json __pycache__ src/**/__pycache__ .pytest_cache; \
		rm -rf *.egg-info build dist; \
		echo "🧪 Recreating virtual environment..."; \
		python3 -m venv env; \
		env/bin/pip install --upgrade pip; \
		env/bin/pip install -r requirements.txt; \
		echo "✅ Reset complete. Fresh environment is ready to use."; \
	else \
		echo "🚫 Cancelled."; \
	fi