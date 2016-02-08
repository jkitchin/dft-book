from jasp import *
with jasp('bulk/Al-lda-vasp') as calc:
    atoms = calc.get_atoms()
with jasp('bulk/Al-lda-ase') as calc:
    atoms2 = calc.get_atoms()
import numpy as np
cellA = atoms.get_cell()
cellB = atoms2.get_cell()
print (np.abs(cellA - cellB) < 0.01).all()