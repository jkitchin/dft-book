from vasp import Vasp
from ase import Atom, Atoms
calc = Vasp('bulk/CuO')
calc.clone('bulk/CuO-U=4.0')
calc.set(ldau=True,   # turn DFT+U on
         ldautype=2,  # select simplified rotationally invariant option
         ldau_luj={'Cu':{'L':2,  'U':4.0, 'J':0.0},
                   'O':{'L':-1, 'U':0.0, 'J':0.0}},
         ldauprint=1,
         ibrion=-1,  #do not rerelax
         nsw=0)
atoms = calc.get_atoms()
print(atoms.get_potential_energy())