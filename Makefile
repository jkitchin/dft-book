# Jupyter Book Makefile for DFT Book
# See https://jupyterbook.org/

.PHONY: html pdf clean serve help run-notebooks venv sync install-claude install-uv

# Default target
all: html

# Create and sync the uv virtual environment
venv:
	uv sync

# Alias for venv
sync: venv

# Build HTML version
html: venv
	uv run jupyter-book build .

# Build PDF via LaTeX
pdf: venv
	uv run jupyter-book build . --builder pdflatex

# Clean build artifacts
clean:
	jupyter-book clean . 2>/dev/null || true
	rm -rf _build

# Serve the book locally for development
serve: html
	uv run python -m http.server --directory _build/html 8000

# Full rebuild (clean + build)
rebuild: clean html

# Run all notebooks in place using uv environment (background process)
run-notebooks: venv
	nohup uv run jupyter nbconvert --to notebook --execute --inplace notebooks/*.ipynb > notebooks.log 2>&1 &
	@echo "Notebooks running in background. Check notebooks.log for progress."

# Run notebooks in foreground (useful for debugging)
run-notebooks-fg: venv
	uv run jupyter nbconvert --to notebook --execute --inplace notebooks/*.ipynb

help:
	@echo "Jupyter Book build targets:"
	@echo "  html           - Build HTML version (default)"
	@echo "  pdf            - Build PDF via LaTeX"
	@echo "  clean          - Remove build artifacts"
	@echo "  serve          - Build and serve locally on port 8000"
	@echo "  rebuild        - Clean and rebuild HTML"
	@echo "  venv/sync      - Create/sync uv virtual environment"
	@echo "  run-notebooks  - Execute all notebooks in background (logs to notebooks.log)"
	@echo "  run-notebooks-fg - Execute all notebooks in foreground"
	@echo "  install-claude - Install Claude CLI"
	@echo "  install-uv     - Install uv package manager"

# Install Claude CLI
install-claude:
	curl -fsSL https://claude.ai/install.sh | bash

# Install uv package manager
install-uv:
	curl -LsSf https://astral.sh/uv/install.sh | sh
