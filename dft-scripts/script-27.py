from ase import Atoms, Atom
from vasp import Vasp
calc = Vasp('molecules/simple-co')
print('energy = {0} eV'.format(calc.get_atoms().get_potential_energy()))
# This creates the directory and makes it current working directory
calc.clone('molecules/clone-1')
calc.set(encut=325)  # this will trigger a new calculation
print('energy = {0} eV'.format(calc.get_atoms().get_potential_energy()))