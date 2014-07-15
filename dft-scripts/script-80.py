from ase.lattice.compounds import NaCl
from ase.io import write
atoms = NaCl(['Na','Cl'], latticeconstant=5.65)
write('images/NaCl.png', atoms, show_unit_cell=2, rotation='45x,45y,45z')