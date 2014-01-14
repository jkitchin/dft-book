from jasp import *
from ase.lattice.surface import fcc110
from ase.io import write
from ase.constraints import FixAtoms
atoms = fcc110('Au', size=(2,1,6), vacuum=10.0)
del atoms[11] # delete surface row
constraint = FixAtoms(mask=[atom.tag > 2 for atom in atoms])
atoms.set_constraint(constraint)
write('images/Au-110-missing-row.png', atoms.repeat((2,2,1)), rotation='-90x', show_unit_cell=2)
with jasp('surfaces/Au-110-missing-row',
          xc='PBE',
          kpts=(6,6,1),
          encut=350,
          ibrion=2,
          isif=2,
          nsw=10,
          atoms=atoms) as calc:
    calc.calculate()