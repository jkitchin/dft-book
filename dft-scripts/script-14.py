from ase.structure import molecule
import numpy as np
# ammonia
atoms = molecule('NH3')
  # cartesian coordinates
print('COM1 = {0}'.format(atoms.get_center_of_mass()))
# compute the center of mass by hand
pos = atoms.positions
masses = atoms.get_masses()
COM = np.array([0., 0., 0.])
for m, p in zip(masses, pos):
    COM += m*p
COM /= masses.sum()
print('COM2 = {0}'.format(COM))
# one-line linear algebra definition of COM
print('COM3 = {0}'.format(np.dot(masses, pos) / np.sum(masses)))