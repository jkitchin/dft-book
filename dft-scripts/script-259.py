from ase.lattice.surface import fcc111
import numpy as np
np.set_printoptions(precision=3,suppress=True)
slab = fcc111('Pd',
              a=3.92,       # Pd lattice constant
              size=(2,2,3), #3-layer slab in 1x1 configuration
              vacuum=10.0)
pos = slab.get_positions() #these positions use x,y,z vectors as a basis
# we want to see the atoms in terms of the unitcell vectors
newbasis = slab.get_cell()
s = np.dot(np.linalg.inv(newbasis.T),pos.T).T
print('Coordinates in new basis are: \n',s)
# what we just did is equivalent to the following atoms method
print('Scaled coordinates from ase are: \n',slab.get_scaled_positions())