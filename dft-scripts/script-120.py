from vasp import Vasp
atoms = Vasp('bulk/Al-lda-vasp').get_atoms()
atoms2 = Vasp('bulk/Al-lda-ase').get_atoms()
import numpy as np
cellA = atoms.get_cell()
cellB = atoms2.get_cell()
print((np.abs(cellA - cellB) < 0.01).all())