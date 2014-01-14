from ase.io import read, write
atoms = read('surfaces/Pt-slab-O-bridge/POSCAR')
write('images/Pt-o-brige-ori.png', atoms, show_unit_cell=2)
atoms = read('surfaces/Pt-slab-O-bridge/CONTCAR')
write('images/Pt-o-brige-final.png', atoms, show_unit_cell=2)