from jasp import *
from ase.structure import molecule
atoms = molecule('H2O')
atoms.center(vacuum=6)
with jasp('molecules/h2o-bader',
          xc='PBE',
          encut=350,
          atoms=atoms) as calc:
    calc.calculate()
    os.system('bader -p all_atom -p atom_index CHG')