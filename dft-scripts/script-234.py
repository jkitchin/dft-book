from vasp import Vasp
print('D = {} eV'.format(2 * Vasp('molecules/H-beef').potential_energy -
                         Vasp('molecules/H2-beef').potential_energy))