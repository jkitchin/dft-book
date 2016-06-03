from ase.io import read, write
atoms = read('bulk/Ru2O4_1.cif')
write('images/Ru2O4.png', atoms, show_unit_cell=2)