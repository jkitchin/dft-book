from ase import Atoms, Atom
from jasp import *
atoms = Atoms([Atom('H', [0.5960812, -0.7677068, 0.0000000]),
               Atom('O', [0.0000000,  0.0000000, 0.0000000]),
               Atom('H', [0.5960812,  0.7677068, 0.0000000])],
              cell=(8, 8, 8))
with jasp('molecules/h2o_relax',
          xc='PBE',
          encut=400,
          ismear=0,  # Gaussian smearing
          ibrion=2,
          ediff=1e-8,
          nsw=10,
          atoms=atoms) as calc:
    print "forces"
    print '======='
    print atoms.get_forces()