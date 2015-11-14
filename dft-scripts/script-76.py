# compute initial and final states
from ase import Atoms
from ase.structure import molecule
import numpy as np
from jasp import *
from ase.constraints import FixAtoms
atoms = molecule('NH3')
constraint = FixAtoms(mask=[atom.symbol == 'N' for atom in atoms])
atoms.set_constraint(constraint)
Npos = atoms.positions[0]
# move N to origin
atoms.translate(-Npos)
atoms.set_cell((10, 10, 10), scale_atoms=False)
atoms2 = atoms.copy()
pos2 = atoms2.positions
for i,atom in enumerate(atoms2):
    if atom.symbol == 'H':
        # reflect through z
        pos2[i] *= np.array([1, 1, -1])
atoms2.positions = pos2
#now move N to center of box
atoms.translate([5, 5, 5])
atoms2.translate([5, 5, 5])
with jasp('molecules/nh3-initial',
          xc='PBE',
          encut=350,
          ibrion=1,
          nsw=10,
          atoms=atoms) as calc:
    try:
        calc.calculate()
    except (VaspSubmitted, VaspQueued):
        pass
with jasp('molecules/nh3-final',
          xc='PBE',
          encut=350,
          ibrion=1,
          nsw=10,
          atoms=atoms2) as calc:
    try:
        calc.calculate()
    except (VaspSubmitted, VaspQueued):
        pass