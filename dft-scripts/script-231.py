import numpy as np
a1 = [2, 0, 0]
a2 = [1, 1, 0]
a3 = [0, 0, 10]
uc = np.array([a1, a2, a3])
print 'V = {0} ang^3 from dot/cross'.format(np.dot(np.cross(a1,a2),a3))
print 'V = {0} ang^3 from det'.format(np.linalg.det(uc))
from ase import Atoms
atoms = Atoms([],cell=uc) #empty list of atoms
print 'V = {0} ang^3 from get_volume'.format(atoms.get_volume())