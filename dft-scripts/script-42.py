from vasp import Vasp
from ase.db import connect
bond_lengths = [1.05, 1.1, 1.15, 1.2, 1.25]
calcs = [Vasp('molecules/co-{0}'.format(d)) for d in bond_lengths]
con = connect('co-database.db', append=False)
for atoms in [calc.get_atoms() for calc in calcs]:
    con.write(atoms)