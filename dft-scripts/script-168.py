from ase.lattice.surface import fcc111
from ase.units import J, m
import numpy as np
slab = fcc111('Cu', size=(1, 1, 3), vacuum=10.0)
cell = slab.get_cell()
area = np.linalg.norm(np.cross(cell[0], cell[1]))
sigma = 0.48  # eV/atom
print 'sigma = {0} J/m^2'.format(sigma / area / (J / m**2))