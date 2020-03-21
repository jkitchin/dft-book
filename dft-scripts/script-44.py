from ase.io import read
ATOMS = read('co-database.db', ':')
print([a[0].x - a[1].x for a in ATOMS])
print([atoms.get_potential_energy() for atoms in ATOMS])