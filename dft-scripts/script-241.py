from vasp import Vasp
from ase.db import connect
calc = Vasp('molecules/simple-co')
atoms = calc.get_atoms()
print calc.results
con = connect('example-1.db')
con.write(atoms)