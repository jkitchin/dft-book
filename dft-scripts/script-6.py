from ase.io import read, write
atoms = read('molecules/isobutane.xyz')
atoms.center(vacuum=5)
write('images/isobutane-xyz.png', atoms, show_unit_cell=2)