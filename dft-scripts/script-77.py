# Run NH3 NEB calculations
from jasp import *
from ase.neb import NEB
with jasp('molecules/nh3-initial') as calc:
    atoms = calc.get_atoms()
with jasp('molecules/nh3-final') as calc:
    atoms2 = calc.get_atoms()
# 5 images including endpoints
images = [atoms]   # initial state
images += [atoms.copy() for i in range(3)]
images += [atoms2]  # final state
neb = NEB(images)
neb.interpolate()
with jasp('molecules/nh3-neb',
          xc='PBE',
          ibrion=1,
          nsw=90,
          spring=-5, debug=logging.DEBUG,
          atoms=images) as calc:
    images, energies = calc.get_neb()
    calc.plot_neb(show=False)
import matplotlib.pyplot as plt
plt.savefig('images/nh3-neb.png')
plt.show()