from vasp import Vasp
from ase.structure import molecule
benzene = molecule('C6H6')
benzene.center(vacuum=5)
print(Vasp('molecules/benzene-pbe',
           xc='PBE',
           encut=350,
           kpts=[1, 1, 1],
           ibrion=1,
           nsw=100,
           atoms=benzene).potential_energy)