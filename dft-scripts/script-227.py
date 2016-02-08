from jasp import *
from ase.structure import molecule
atoms = molecule('CO')
atoms.center(vacuum=5)
with jasp('molecules/CO-vacuum',
          encut=600,
          prec='Accurate',
          ismear=0,
          sigma=0.05,
          ibrion=2,
          nsw=0,
          ediff=1e-6,
          atoms=atoms) as calc:
    print(atoms.get_potential_energy())
    print(atoms.get_forces())
    print('Calculation time: {} seconds'.format(calc.get_elapsed_time()))