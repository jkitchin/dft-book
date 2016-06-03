from ase.structure import molecule
# ammonia
atoms = molecule('NH3')
print('atom symbol')
print('===========')
for i, atom in enumerate(atoms):
    print('{0:2d} {1:3s}' .format(i, atom.symbol))
# N-H bond length
s = 'The N-H distance is {0:1.3f} angstroms'
print(s.format(atoms.get_distance(0, 1)))