from ase.lattice.hexagonal import Graphite
from ase.io import write
atoms = Graphite('C', latticeconstant={'a':2.4612, 'c':6.7079})
write('images/graphite.png', atoms.repeat((2,2,1)),rotation='115x', show_unit_cell=2)
write('images/graphite-top.png', atoms.repeat((2,2,1)), show_unit_cell=2)