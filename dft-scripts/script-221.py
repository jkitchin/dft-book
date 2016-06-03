from vasp import Vasp
e1, e2, e3 = [Vasp(wd).potential_energy
              for wd in ['surfaces/Au-benzene-pbe',
                         'surfaces/Au-pbe',
                         'molecules/benzene-pbe']]
print('PBE adsorption energy = {} eV'.format(e1 - e2 - e3))