from jasp import *
with jasp('surfaces/Au-benzene-pbe') as calc:
    e1 = calc.get_atoms().get_potential_energy()
with jasp('surfaces/Au-pbe') as calc:
    e2 = calc.get_atoms().get_potential_energy()
with jasp('molecules/benzene-pbe') as calc:
    e3 = calc.get_atoms().get_potential_energy()
print('PBE adsorption energy = {} eV'.format(e1 - e2 - e3))