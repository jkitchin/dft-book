from ase import Atom, Atoms
from vasp import Vasp
co = Atoms([Atom('C',[0, 0, 0]),
            Atom('O',[1.2, 0, 0])],
            cell=(6, 6, 6))
calc = Vasp('molecules/co-cg',
          xc='PBE',
          nbands=6,
          encut=350,
          ismear=1,
          sigma=0.01, # this is small for a molecule
          ibrion=2,   # conjugate gradient optimizer
          nsw=5,      # do at least 5 steps to relax
          atoms=co)
print('Forces')
print('=======')
print(co.get_forces())
pos = co.get_positions()
d = ((pos[0] - pos[1])**2).sum()**0.5
print('Bondlength = {0:1.2f} angstroms'.format(d))