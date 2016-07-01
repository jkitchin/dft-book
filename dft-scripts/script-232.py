from vasp import Vasp
alloy_0 = Vasp('bulk/CuPd-cls-0').potential_energy
alloy_1 = Vasp('bulk/CuPd-cls-1').potential_energy
ref_0 = Vasp('bulk/Cu-cls-0').potential_energy
ref_1 = Vasp('bulk/Cu-cls-1').potential_energy
CLS = (alloy_1 - alloy_0) - (ref_1 - ref_0)
print('CLS = {} eV'.format(CLS))