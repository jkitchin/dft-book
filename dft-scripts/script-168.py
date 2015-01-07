from jasp import *
from ase.lattice.surface import fcc111
from ase.constraints import FixAtoms
atoms = fcc111('Pt', size=(2,2,3), vacuum=10.0)
constraint = FixAtoms(mask=[True for atom in atoms])
atoms.set_constraint(constraint)
from ase.io import write
write('images/Pt-fcc-ori.png', atoms, show_unit_cell=2)
with jasp('surfaces/Pt-slab',
          xc='PBE',
          kpts=(4, 4, 1),
          encut=350,
          atoms=atoms) as calc:
    print atoms.get_potential_energy()