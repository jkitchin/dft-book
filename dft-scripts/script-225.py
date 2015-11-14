from jasp import *
from ase.structure import molecule
H = molecule('H')
H.set_cell([8, 8, 8], scale_atoms=False)
with jasp('molecules/H-beef',
          xc='PBE', gga='BF',
          encut=350,
          ismear=0,
          atoms=H) as calc:
    try:
        eH = H.get_potential_energy()
        print(eH)
    except (VaspSubmitted, VaspQueued):
        print('running or queued')
        eH = None