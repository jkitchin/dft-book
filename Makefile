# Jupyter Book Makefile for DFT Book
# See https://jupyterbook.org/

.PHONY: html pdf clean serve help

# Default target
all: html

# Build HTML version
html:
	jupyter-book build .

# Build PDF via LaTeX
pdf:
	jupyter-book build . --builder pdflatex

# Clean build artifacts
clean:
	jupyter-book clean .
	rm -rf _build

# Serve the book locally for development
serve: html
	python -m http.server --directory _build/html 8000

# Full rebuild (clean + build)
rebuild: clean html

help:
	@echo "Jupyter Book build targets:"
	@echo "  html    - Build HTML version (default)"
	@echo "  pdf     - Build PDF via LaTeX"
	@echo "  clean   - Remove build artifacts"
	@echo "  serve   - Build and serve locally on port 8000"
	@echo "  rebuild - Clean and rebuild HTML"
