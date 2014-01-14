from jasp import *
from ase.lattice.surface import fcc111
from ase.constraints import FixAtoms
atoms = fcc111('Al', size=(1,1,4), vacuum=10.0)
constraint = FixAtoms(mask=[atom.tag >= 3 for atom in atoms])
atoms.set_constraint(constraint)
with jasp('surfaces/Al-slab-relaxed',
          xc='PBE',
          kpts=(6,6,1),
          encut=350,
          ibrion=2,
          isif=2,
          nsw=10, debug=logging.DEBUG,
          atoms=atoms) as calc:
    calc.calculate()
    print calc