# calculate O atom energy in orthorhombic boxes
from vasp import Vasp
from ase import Atom, Atoms
# orthorhombic box origin
atoms = Atoms([Atom('O', [0, 0, 0], magmom=2)],
              cell=(8, 9, 10))
calc = Vasp('molecules/O-orthorhombic-box-origin',
            xc='PBE',
            encut=400,
            ismear=0,
            sigma=0.01,
            ispin=2,
            atoms=atoms)
print('Orthorhombic box (origin): E = {0} eV'.format(atoms.get_potential_energy()))
# orthorhombic box center
atoms = Atoms([Atom('O', [4, 4.5, 5], magmom=2)],
              cell=(8, 9, 10))
calc = Vasp('molecules/O-orthorhombic-box-center',
            xc='PBE',
            encut=400,
            ismear=0,
            sigma=0.01,
            ispin=2,
            atoms=atoms)
print('Orthorhombic box (center): E = {0} eV'.format(atoms.get_potential_energy()))
# orthorhombic box random
atoms = Atoms([Atom('O', [2.13, 7.32, 1.11], magmom=2)],
              cell=(8, 9, 10))
calc = Vasp('molecules/O-orthorhombic-box-random',
            xc='PBE',
            encut=400,
            ismear=0,
            sigma=0.01,
            ispin=2,
            atoms=atoms)
print('Orthorhombic box (random): E = {0} eV'.format(atoms.get_potential_energy()))