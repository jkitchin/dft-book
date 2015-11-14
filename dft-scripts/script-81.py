from ase.io import write
from ase.lattice.cubic import FaceCenteredCubic
atoms = FaceCenteredCubic(directions=[[1, 0, 0],
                                      [0, 1, 0],
                                      [0, 0, 1]],
                          size=(1, 1, 1),
                          symbol='Ag',
                          latticeconstant=4.0)
write('images/Ag-bulk.png', atoms, show_unit_cell=2)
# to make an alloy, we can replace one atom with another kind
atoms[0].symbol = 'Pd'
write('images/AgPd-bulk.png', atoms, show_unit_cell=2)