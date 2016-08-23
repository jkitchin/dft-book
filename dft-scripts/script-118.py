from vasp import Vasp
from ase.lattice import bulk
Al = bulk('Al', 'fcc', a=4.5, cubic=True)
calc = Vasp('bulk/Al-lda-vasp',
            xc='LDA', isif=7, nsw=5,
            ibrion=1, ediffg=-1e-3,
            lwave=False, lcharg=False,
            atoms=Al)
print(calc.potential_energy)
print(calc)