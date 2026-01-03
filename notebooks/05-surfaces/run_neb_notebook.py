#!/usr/bin/env python3
"""Run the NEB notebook."""
import subprocess
import sys
import os

os.chdir('/home/jovyan/dft-book/notebooks/05-surfaces')

result = subprocess.run([
    sys.executable, '-m', 'jupyter', 'nbconvert',
    '--to', 'notebook',
    '--execute',
    '--inplace',
    '10-surface-diffusion-barrier.ipynb',
    '--ExecutePreprocessor.timeout=900'
], capture_output=False)

sys.exit(result.returncode)
