from jasp import *
with jasp('bulk/CuPd-cls-0') as calc:
    alloy_0 = calc.get_atoms().get_potential_energy()
with jasp('bulk/CuPd-cls-1') as calc:
    alloy_1 = calc.get_atoms().get_potential_energy()
with jasp('bulk/Cu-cls-0') as calc:
    ref_0 = calc.get_atoms().get_potential_energy()
with jasp('bulk/Cu-cls-1') as calc:
    ref_1 = calc.get_atoms().get_potential_energy()
CLS = (alloy_1 - alloy_0) - (ref_1 - ref_0)
print('CLS = {} eV'.format(CLS))