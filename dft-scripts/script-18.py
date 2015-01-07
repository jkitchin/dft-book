from ase.structure import molecule
# ammonia
atoms = molecule('NH3')
print 'atom symbol'
print '==========='
for i, atom in enumerate(atoms):
    print '{0:2d} {1:3s}'.format(i, atom.symbol)
a = atoms.positions[0] - atoms.positions[1]
b = atoms.positions[0] - atoms.positions[2]
from numpy import arccos, dot, pi
from numpy.linalg import norm
theta_rad = arccos(dot(a, b) / (norm(a) * norm(b)))  # in radians
print 'theta = {0:1.1f} degrees'.format(theta_rad * 180./pi)