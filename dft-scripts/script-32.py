from jasp import *
from ase.units import Debye
with jasp('molecules/co-centered') as calc:
    dipole_vector = calc.get_dipole_moment()
    dipole_moment = ((dipole_vector**2).sum())**0.5/Debye
    print('The dipole moment is {0:1.2f} Debye'.format(dipole_moment))