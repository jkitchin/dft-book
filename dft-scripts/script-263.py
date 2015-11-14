from ase import Atoms, Atom
from jasp import *
atoms = Atoms([Atom('O',[5, 5, 5], magmom=1)],
             cell=(6, 6, 6))
with jasp('molecules/O_sv',
          encut=300,
          xc='PBE',
          ispin=2,
          ismear=0,
          sigma=0.001,
          setups={'O':'_sv'}, # specifies O_sv potential
          atoms=atoms) as calc:
    print('Total energy = {0} eV'.format(atoms.get_potential_energy()))