from ase.structure import molecule
atoms = molecule('C6H6')  # benzene
# access properties on each atom
print(' #  sym   p_x     p_y     p_z')
print('------------------------------')
for i, atom in enumerate(atoms):
   print('{0:3d}{1:^4s}{2:-8.2f}{3:-8.2f}{4:-8.2f}'.format(i,
                                                           atom.symbol,
                                                           atom.x,
                                                           atom.y,
                                                           atom.z))
# get all properties in arrays
sym = atoms.get_chemical_symbols()
pos = atoms.get_positions()
num = atoms.get_atomic_numbers()
atom_indices = range(len(atoms))
print()
print('  # sym    at#    p_x     p_y     p_z')
print('-------------------------------------')
for i, s, n, p in zip(atom_indices, sym, num, pos):
    px, py, pz = p
    print('{0:3d}{1:>3s}{2:8d}{3:-8.2f}{4:-8.2f}{5:-8.2f}'.format(i, s, n,
                                                                  px, py, pz))