from ase.structure import molecule
import numpy as np
atoms = molecule('CH3Cl')
moments, axes = atoms.get_moments_of_inertia(vectors=True)
print 'Moments = {0}'.format(moments)
print 'axes = {0}'.format(axes)