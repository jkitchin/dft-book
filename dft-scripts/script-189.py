from jasp import *
from ase import Atom, Atoms
with jasp('bulk/Cu2O') as calc:
    calc.clone('bulk/Cu2O-U=4.0')
with jasp('bulk/Cu2O-U=4.0') as calc:
    calc.set(ldau=True,   # turn DFT+U on
             ldautype=2,  # select simplified rotationally invariant option
             ldau_luj={'Cu':{'L':2,  'U':4.0, 'J':0.0},
                        'O':{'L':-1, 'U':0.0, 'J':0.0}},
             ldauprint=1,
             ibrion=-1,  #do not rerelax
             nsw=0)
    calc.calculate()
    print calc