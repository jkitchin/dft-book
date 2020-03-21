from ase.io import write
from ase.lattice.cubic import FaceCenteredCubic
atoms = FaceCenteredCubic('Ag', directions=[[0, 1, 1],
                                            [1, 0, 1],
                                            [1, 1, 0]])
write('images/Ag-fcc-primitive.png', atoms, show_unit_cell=2)
print atoms