from jasp import *
from ase import Atoms, Atom
import numpy as np
np.set_printoptions(precision=3, suppress=True)
atoms = Atoms([Atom('C', [0, 0, 0]),
               Atom('O', [1.2, 0, 0])])
L = [4, 5, 6, 8, 10]
volumes, energies = [], []
ready = True
for a in L:
    atoms.set_cell([a, a, a], scale_atoms=False)
    atoms.center()
    with jasp('molecules/co-L-{0}'.format(a),
              encut=350,
              xc='PBE',
              atoms=atoms) as calc:
        try:
            energies.append(atoms.get_potential_energy())
        except (VaspSubmitted, VaspQueued):
            ready = False
if not ready:
    import sys; sys.exit()
import matplotlib.pyplot as plt
plt.plot(L, energies, 'bo-')
plt.xlabel('Unit cell length ($\AA$)')
plt.ylabel('Total energy (eV)')
plt.savefig('images/co-e-v.png')
plt.show()