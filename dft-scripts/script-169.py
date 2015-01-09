# compute local potential of slab with no dipole
from ase.lattice.surface import fcc111, add_adsorbate
from jasp import *
import matplotlib.pyplot as plt
from ase.io import write
slab = fcc111('Al', size=(2, 2, 2), vacuum=10.0)
add_adsorbate(slab, 'Na', height=1.2, position='fcc')
slab.center()
write('images/Na-Al-slab.png', slab, rotation='-90x', show_unit_cell=2)
with jasp('surfaces/Al-Na-nodip',
          xc='PBE',
          encut=340,
          kpts=(2, 2, 1),
          lvtot=True,  # write out local potential
          lvhar=True,  # write out only electrostatic potential, not xc pot
          atoms=slab) as calc:
    calc.calculate()