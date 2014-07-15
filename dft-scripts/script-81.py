from ase.lattice.spacegroup import crystal
# FCC aluminum
a = 4.05
al = crystal('Al', [(0,0,0)], spacegroup=225, cellpar=[a, a, a, 90, 90, 90])
print al