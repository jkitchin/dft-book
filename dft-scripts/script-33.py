from vasp import Vasp
from ase.units import Debye
calc = Vasp('molecules/co-centered')
dipole_moment = calc.get_dipole_moment()
print('The dipole moment is {0:1.2f} Debye'.format(dipole_moment))