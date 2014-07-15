from ase.lattice.surface import fcc111
from ase.io import write
slab = fcc111('Al', size=(2,2,3), vacuum=10.0)
write('images/Al-slab.png', slab, rotation='90x',show_unit_cell=2)