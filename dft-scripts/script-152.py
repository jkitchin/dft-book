from ase.lattice.surface import fcc111
from ase.io import write
from ase.visualize import view
slab = fcc111('Al', size=(2, 2, 3), vacuum=10.0)
from ase.constraints import FixAtoms
constraint = FixAtoms(mask=[atom.tag >= 2 for atom in slab])
slab.set_constraint(constraint)
view(slab)
write('images/Al-slab.png', slab, rotation='90x', show_unit_cell=2)