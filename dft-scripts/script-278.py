from vasp import Vasp
from vasp.vasprc import VASPRC
VASPRC['queue.ppn']=4
from ase import Atom, Atoms
atoms = Atoms([Atom('O',[5, 5, 5], magmom=1)],
             cell=(6, 6, 6))
calc = Vasp('molecules/O_s-4nodes',
          encut=300,
          xc='PBE',
          ispin=2,
          ismear=0,
          sigma=0.001,
          setups=[['O', '_s']],  # specifies O_s potential
          atoms=atoms)
print calc.potential_energy