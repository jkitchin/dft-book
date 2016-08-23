from vasp import Vasp
from ase.lattice import bulk
from ase.optimize import BFGS as QuasiNewton
Al = bulk('Al', 'fcc', a=4.5, cubic=True)
calc = Vasp('bulk/Al-lda-ase',
            xc='LDA',
            atoms=Al)
from ase.constraints import StrainFilter
sf = StrainFilter(Al)
qn = QuasiNewton(sf, logfile='relaxation.log')
qn.run(fmax=0.1, steps=5)
print('Stress:\n', calc.stress)
print('Al post ASE volume relaxation\n', calc.get_atoms().get_cell())
print(calc)