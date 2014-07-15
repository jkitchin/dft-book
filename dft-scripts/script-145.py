from jasp import *
from ase import Atom, Atoms
atoms = Atoms([Atom('Fe',[0.00,  0.00,  0.00], magmom=5),
               Atom('Fe',[4.3,   4.3,   4.3],  magmom=-5),
               Atom('O', [2.15,  2.15,  2.15], magmom=0),
               Atom('O', [6.45,  6.45,  6.45], magmom=0)],
               cell=[[4.3,    2.15,    2.15],
                     [2.15,    4.3,     2.15],
                     [2.15,    2.15,    4.3]])
with jasp('bulk/afm-feo',
          encut=350,
          prec='Normal',
          ispin=2,
          nupdown=0, # this forces a non-magnetic solution
          lorbit=11, # to get individual moments
          lreal=False,
          atoms=atoms) as calc:
    print 'Magnetic moments = ',atoms.get_magnetic_moments()
    print 'Total magnetic moment = ',atoms.get_magnetic_moment()