from ase import Atoms, Atom
from ase.io import write
# define an Atoms object
atoms = Atoms([Atom('C', [0., 0., 0.]),
               Atom('O', [1.1, 0., 0.])],
              cell=(10, 10, 10))
print 'V = {0:1.0f} Angstrom^3'.format(atoms.get_volume())
write('images/simple-cubic-cell.png', atoms, show_unit_cell=2)