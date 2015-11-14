from jasp import *
from ase.lattice import bulk
from ase.optimize import BFGS as QuasiNewton
Al = bulk('Al', 'fcc', a=4.5, cubic=True)
with jasp('bulk/Al-lda-ase',
          xc='LDA',
          atoms=Al) as calc:
    from ase.constraints import StrainFilter
    sf = StrainFilter(Al)
    qn = QuasiNewton(sf, logfile='relaxation.log')
    qn.run(fmax=0.1, steps=5)
    print 'Stress:\n', calc.read_stress()
    print 'Al post ASE volume relaxation\n', calc.get_atoms().get_cell()
    print calc