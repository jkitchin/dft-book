from jasp import *
from ase.lattice.surface import fcc111, add_adsorbate
from ase.constraints import FixAtoms
from ase.io import write
atoms = fcc111('Pt', size=(1, 1, 3), vacuum=10.0)
# note this function only works when atoms are created by the surface module.
add_adsorbate(atoms, 'O', height=1.2, position='fcc')
constraint = FixAtoms(mask=[atom.symbol != 'O' for atom in atoms])
atoms.set_constraint(constraint)
write('images/Pt-o-fcc-1ML.png', atoms, show_unit_cell=2)
with jasp('surfaces/Pt-slab-1x1-O-fcc',
          xc='PBE',
          kpts=(8, 8, 1),
          encut=350,
          ibrion=2,
          nsw=25,
          atoms=atoms) as calc:
    print atoms.get_potential_energy()