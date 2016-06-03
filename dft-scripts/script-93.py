from ase.lattice.spacegroup import crystal
a = 4.6
c = 2.95
rutile = crystal(['Ti', 'O'], basis=[(0, 0, 0), (0.3, 0.3, 0.0)],
                 spacegroup=136, cellpar=[a, a, c, 90, 90, 90])
print rutile