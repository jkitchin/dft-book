from ase.io import write
from ase.lattice.cubic import FaceCenteredCubic
atoms = FaceCenteredCubic('Ag')
write('images/Ag-fcc.png', atoms, show_unit_cell=2)
print atoms