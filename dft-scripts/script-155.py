from jasp import *
from ase.lattice.surface import fcc111
atoms = fcc111('Al', size=(1, 1, 4), vacuum=10.0)
with jasp('surfaces/Al-slab-unrelaxed',
          xc='PBE',
          kpts=(6, 6, 1),
          encut=350,
          atoms=atoms) as calc:
    atoms.get_forces()
    print calc