from vasp import Vasp
from ase import Atom, Atoms
# square box origin
atoms = Atoms([Atom('O', [0, 0, 0], magmom=2)],
              cell=(10, 10, 10))
pars = dict(xc='PBE',
            encut=400,
            ismear=0,
            sigma=0.01,
            ispin=2)
calc = Vasp('molecules/O-square-box-origin',
            atoms=atoms, **pars)
print('Square box (origin): E = {0} eV'.format(atoms.get_potential_energy()))
# square box center
atoms = Atoms([Atom('O', [5, 5, 5], magmom=2)],
              cell=(10, 10, 10))
calc = Vasp('molecules/O-square-box-center',
            atoms=atoms, **pars)
print('Square box (center): E = {0} eV'.format(atoms.get_potential_energy()))
# square box random
atoms = Atoms([Atom('O', [2.13, 7.32, 1.11], magmom=2)],
              cell=(10, 10, 10))
calc = Vasp('molecules/O-square-box-random',
            atoms=atoms, **pars)
print('Square box (random): E = {0} eV'.format(atoms.get_potential_energy()))