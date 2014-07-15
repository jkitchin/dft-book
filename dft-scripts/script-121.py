from jasp import *
from ase import Atom, Atoms
atoms = Atoms([Atom('Cu',  [0.000,      0.000,      0.000]),
               Atom('Pd',  [-1.652,     0.000,      2.039])],
              cell=  [[ 0.000, -2.039,  2.039],
                      [ 0.000,  2.039,  2.039],
                      [ -3.303,  0.000,  0.000]])
with jasp('bulk/alloy/cupd-1',
          xc='PBE',
          encut=350,
          kpts=(12,12,8),
          nbands=17,
          ibrion=2,
          isif=3,
          nsw=10,
          atoms=atoms) as calc:
    cupd1 = atoms.get_potential_energy()
atoms = Atoms([Atom('Cu',  [-0.049,     0.049,      0.049]),
               Atom('Cu',  [-11.170,   11.170,     11.170]),
               Atom('Pd',  [-7.415,     7.415,      7.415]),
               Atom('Pd',  [-3.804 ,    3.804,      3.804])],
              cell=[[-5.629,  3.701,  5.629 ],
                    [-3.701,  5.629,  5.629 ],
                    [-5.629,  5.629,  3.701 ]])
with jasp('bulk/alloy/cupd-2',
          xc='PBE',
          encut=350,
          kpts=(8,8,8),
          nbands=34,
          ibrion=2,
          isif=3,
          nsw=10,
          atoms=atoms) as calc:
    cupd2 = atoms.get_potential_energy()
print 'cupd-1 = {0} eV'.format(cupd1)
print 'cupd-2 = {0} eV'.format(cupd2)