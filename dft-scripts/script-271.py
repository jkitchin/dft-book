from ase.lattice.cubic import BodyCenteredCubic
import numpy as np
bulk = BodyCenteredCubic(directions=[[1,0,0],
                                     [0,1,0],
                                     [0,0,1]],
                         size=(2,2,2),
                         latticeconstant=2.87,
                         symbol='Fe')
newbasis = 2.87*np.array([[-0.5, 0.5, 0.5],
                          [0.5, -0.5, 0.5],
                          [0.5, 0.5, -0.5]])
pos = bulk.get_positions()
s = np.dot(np.linalg.inv(newbasis.T), pos.T).T
print('atom positions in primitive basis')
print(s)
# let us see the unit cell in terms of the primitive basis too
print('unit cell in terms of the primitive basis')
print(np.dot(np.linalg.inv(newbasis.T), bulk.get_cell().T).T)