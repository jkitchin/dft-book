from jasp import *
from ase.structure import molecule
benzene = molecule('C6H6')
benzene.center(vacuum=5)
with jasp('molecules/benzene-pbe-d2',
          xc='PBE',
          encut=350,
          kpts=(1,1,1),
          ibrion=1,
          nsw=100,
          lvdw=True,
          atoms=benzene) as calc:
    print(benzene.get_potential_energy())