# Run NH3 NEB calculations
from vasp import Vasp
from ase.neb import NEB
from ase.io import read
atoms = Vasp('molecules/nh3-initial').get_atoms()
atoms2 = Vasp('molecules/nh3-final').get_atoms()
# 5 images including endpoints
images = [atoms]   # initial state
images += [atoms.copy() for i in range(3)]
images += [atoms2]  # final state
neb = NEB(images)
neb.interpolate()
calc = Vasp('molecules/nh3-neb',
            xc='PBE',
            ibrion=1, encut=350,
            nsw=90,
            spring=-5.0,
            atoms=images)
#calc.write_db(atoms, 'molecules/nh3-neb/00/DB.db')
#calc.write_db(atoms2, 'molecules/nh3-neb/04/DB.db')
images, energies = calc.get_neb()
calc.stop_if(None in energies)
print images
print energies
p = calc.plot_neb(show=False)
import matplotlib.pyplot as plt
plt.savefig('images/nh3-neb.png')