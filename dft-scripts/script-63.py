from jasp import *
from ase import Atom, Atoms
# square box origin
atoms = Atoms([Atom('O', [0, 0, 0], magmom=2)],
              cell=(10, 10, 10))
with jasp('molecules/O-square-box-origin',
          xc='PBE',
          encut=400,
          ismear=0,
          sigma=0.01,
          ispin=2,
          atoms=atoms) as calc:
    try:
        print('Square box (origin): E = {0} eV'.format(atoms.get_potential_energy()))
    except (VaspSubmitted, VaspQueued):
        pass
# square box center
atoms = Atoms([Atom('O', [5, 5, 5], magmom=2)],
              cell=(10, 10, 10))
with jasp('molecules/O-square-box-center',
          xc='PBE',
          encut=400,
          ismear=0,
          sigma=0.01,
          ispin=2,
          atoms=atoms) as calc:
    try:
        print('Square box (center): E = {0} eV'.format(atoms.get_potential_energy()))
    except (VaspSubmitted, VaspQueued):
        pass
# square box random
atoms = Atoms([Atom('O', [2.13, 7.32, 1.11], magmom=2)],
              cell=(10, 10, 10))
with jasp('molecules/O-square-box-random',
          xc='PBE',
          encut=400,
          ismear=0,
          sigma=0.01,
          ispin=2,
          atoms=atoms) as calc:
    try:
        print('Square box (random): E = {0} eV'.format(atoms.get_potential_energy()))
    except (VaspSubmitted, VaspQueued):
        pass