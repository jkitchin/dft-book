from ase import Atoms, Atom
import numpy as np
b = 7.1
atoms = Atoms([Atom('C', [0., 0., 0.]),
               Atom('O', [1.1, 0., 0.])],
              cell=[[b, b, 0.],
                    [b, 0., b],
                    [0., b, b]])
# get unit cell vectors and their lengths
(a1, a2, a3) = atoms.get_cell()
print '|a1| = {0:1.2f} Ang'.format(np.sum(a1**2)**0.5)
print '|a2| = {0:1.2f} Ang'.format(np.linalg.norm(a2))
print '|a3| = {0:1.2f} Ang'.format(np.sum(a3**2)**0.5)