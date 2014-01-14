from ase import Atom, Atoms
import numpy as np
a = 3.61 # lattice constant
atoms = Atoms([Atom('Cu', [0,0,0])],
              cell=0.5 * a*np.array([[ 1.0,  1.0, -1.0],
                                     [-1.0,  1.0,  1.0],
                                     [ 1.0, -1.0,  1.0]]))
print 'BCC lattice constant = {0} Ang'.format(a*(11.8/atoms.get_volume())**(1./3.))