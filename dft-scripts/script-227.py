from vasp import Vasp
e1, e2, e3 = [Vasp(wd).potential_energy
              for wd in ['surfaces/Au-benzene-pbe-d2',
                         'surfaces/Au-pbe-d2',
                         'molecules/benzene-pbe-d2']]
print('Adsorption energy = {0:1.2f} eV'.format(e1 - e2 - e3))