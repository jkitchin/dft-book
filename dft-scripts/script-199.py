from vasp import Vasp
from ase.io import write
from ase.lattice.surface import fcc111
from ase.constraints import FixAtoms
atoms = fcc111('Pt', size=(1, 1, 3), vacuum=10.0)
constraint = FixAtoms(mask=[True for atom in atoms])
atoms.set_constraint(constraint)
write('images/Pt-fcc-1ML.png', atoms, show_unit_cell=2)
print(Vasp('surfaces/Pt-slab-1x1',
           xc='PBE',
           kpts=[8, 8, 1],
           encut=350,
           atoms=atoms).potential_energy)