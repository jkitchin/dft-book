from vasp import Vasp
calc = Vasp('molecules/O2-sp-singlet')
print('singlet: {0} eV'.format(calc.potential_energy))
calc = Vasp('molecules/O2-sp-triplet')
print('triplet: {0} eV'.format(calc.potential_energy))