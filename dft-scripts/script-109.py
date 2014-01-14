from jasp import *
from ase.lattice.cubic import FaceCenteredCubic
atoms = FaceCenteredCubic(symbol='Al')
with jasp('bulk/Al-bulk',
          xc='PBE',
          kpts=(12,12,12),
          encut=350,   
          prec='High',       
          isif=3,
          nsw=30,
          ibrion=1,
          atoms=atoms) as calc:
    print atoms.get_potential_energy()
    print atoms.get_stress()