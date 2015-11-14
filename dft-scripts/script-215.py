from jasp import *
with jasp('surfaces/Au-benzene-pbe-d2') as calc:
    e1 = calc.get_atoms().get_potential_energy()
with jasp('surfaces/Au-pbe-d2') as calc:
    e2 = calc.get_atoms().get_potential_energy()
with jasp('molecules/benzene-pbe-d2') as calc:
    e3 = calc.get_atoms().get_potential_energy()
print('Adsorption energy = {0:1.2f} eV'.format(e1 - e2 - e3))