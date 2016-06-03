from ase import Atoms, Atom
from ase.io import write
b = 7.1
atoms = Atoms([Atom('C', [0., 0., 0.]),
               Atom('O', [1.1, 0., 0.])],
              cell=[[b, b, 0.],
                    [b, 0., b],
                    [0., b, b]])
print('V = {0:1.0f} Ang^3'.format(atoms.get_volume()))
atoms.center()  # translate atoms to center of unit cell
write('images/fcc-cell.png', atoms, show_unit_cell=2)