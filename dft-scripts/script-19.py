from ase.data.molecules import molecule
from numpy import pi
# ammonia
atoms = molecule('NH3')
print 'theta = {0} degrees'.format(atoms.get_angle([1,0,2])*180./pi)