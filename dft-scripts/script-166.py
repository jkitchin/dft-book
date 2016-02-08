from jasp import *
from ase.lattice.surface import fcc110
from ase.io import write
from ase.constraints import FixAtoms
atoms = fcc110('Ag', size=(2, 1, 6), vacuum=10.0)
constraint = FixAtoms(mask=[atom.tag > 2 for atom in atoms])
atoms.set_constraint(constraint)
with jasp('surfaces/Ag-110',
          xc='PBE',
          kpts=(6, 6, 1),
          encut=350,
          ibrion=2,
          isif=2,
          nsw=10,
          atoms=atoms) as calc:
    calc.calculate()