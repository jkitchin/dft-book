from vasp import Vasp
from ase import Atom, Atoms
import logging
calc = Vasp('bulk/Cu2O')
calc.clone('bulk/Cu2O-U=4.0')
calc.set(ldau=True,   # turn DFT+U on
         ldautype=2,  # select simplified rotationally invariant option
         ldau_luj={'Cu':{'L':2,  'U':4.0, 'J':0.0},
                   'O':{'L':-1, 'U':0.0, 'J':0.0}},
         ldauprint=1,
         ibrion=-1,  #do not rerelax
         nsw=0)
atoms = calc.get_atoms()
print(atoms.get_potential_energy())
#print calc