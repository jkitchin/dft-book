# Modeling Materials Using Density Functional Theory

A comprehensive guide to computational materials science using Density Functional Theory (DFT) with VASP and the Atomic Simulation Environment (ASE).

**Author:** John Kitchin

## Getting Started

### Prerequisites

- Python 3.10+
- [uv](https://docs.astral.sh/uv/) package manager

### Installation

```bash
# Install dependencies
uv sync

# Activate the environment
source .venv/bin/activate
```

### Building the Book

```bash
# Build HTML version
make html

# Build PDF (requires LaTeX)
make pdf

# Serve locally for development
make serve
```

The built book will be in `_build/html/`.

## Contents

1. Introduction to the Book
2. Introduction to DFT
3. Molecules
4. Bulk Systems
5. Surfaces
6. Atomistic Thermodynamics
7. Advanced Electronic Structure
8. Databases
9. Acknowledgments
10. Appendices
11. Python

## License

The book text and figures are licensed under [CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/). The code (notebooks, scripts, and code blocks) is licensed under the [MIT License](LICENSE). See [LICENSE](LICENSE) for details.

## Citation

If you use this book in your research, please cite:

```
Kitchin, J. R. "Modeling Materials Using Density Functional Theory"
```

Citation metadata is also provided in [CITATION.cff](CITATION.cff).
