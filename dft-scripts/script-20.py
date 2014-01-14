# calculate an ethane dihedral angle
from ase.structure import molecule
import numpy as np
atoms = molecule('C2H6')
print 'atom symbol'
print '==========='
for i, atom in enumerate(atoms):
  print '{0:2d} {1:3s}'.format(i,atom.symbol)
da = atoms.get_dihedral([5,1,0,4])*180./np.pi
print 'dihedral angle = {0:1.2f} degrees'.format(da)