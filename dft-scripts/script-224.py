from jasp import *
with jasp('molecules/H-beef') as calc:
    H = calc.get_atoms()
    eH = H.get_potential_energy()
with jasp('molecules/H2-beef') as calc:
    H2 = calc.get_atoms()
    eH2 = H2.get_potential_energy()
print('D = {} eV'.format(2 * eH - eH2))