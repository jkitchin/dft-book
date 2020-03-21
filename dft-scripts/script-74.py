from vasp import Vasp
from ase import Atom, Atoms
atoms = Atoms([Atom('O', [4, 4.5, 5], magmom=2)],
              cell=(8, 9, 10))
calc = Vasp('molecules/O-sp-triplet-lowsym-s',
          xc='PBE',
            ismear=0,
            ispin=2,
            sigma=0.01,
            setups=[['O', '_s']],
            atoms=atoms)
E_O = atoms.get_potential_energy()
print(E_O)