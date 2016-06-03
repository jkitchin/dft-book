from vasp import Vasp
from ase.structure import molecule
atoms = molecule('H2O')
atoms.center(vacuum=6)
calc = Vasp('molecules/h2o-bader',
            xc='PBE',
            encut=350,
            lcharg=True,
            laechg=True,
            atoms=atoms)
print calc.potential_energy