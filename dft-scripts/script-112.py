from jasp import *
from ase.lattice.cubic import BodyCenteredCubic
atoms = BodyCenteredCubic(symbol='Fe')
for atom in atoms:
    atom.magmom = 3.0
with jasp('bulk/Fe-bulk',
          xc='PBE',
          kpts=(6, 6, 6),
          encut=350,
          ispin=2,
          isif=3,
          nsw=30,
          ibrion=1,
          atoms=atoms) as calc:
    print atoms.get_potential_energy()
    print atoms.get_stress()