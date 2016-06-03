from ase import Atoms, Atom
from vasp import Vasp
atoms = Atoms([Atom('O',[5, 5, 5], magmom=1)],
             cell=(6, 6, 6))
calc = Vasp('molecules/O_s',
          encut=300,
            xc='PBE',
            ispin=2,
            ismear=0,
            sigma=0.001,
            setups=[['O', '_s']], # specifies O_s potential
            atoms=atoms)
print calc.potential_energy