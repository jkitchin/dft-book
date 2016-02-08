# step 1 frozen atoms and shape at different volumes
from ase import Atom, Atoms
import numpy as np
from jasp import *
import matplotlib.pyplot as plt
'''
create a TiO2 structure from the lattice vectors at
http://cst-www.nrl.navy.mil/lattice/struk/c4.html
This site does not exist anymore.
'''
a = 4.59  # experimental degrees of freedom.
c = 2.96
u = 0.3  # internal degree of freedom!
#primitive vectors
a1 = a * np.array([1.0, 0.0, 0.0])
a2 = a * np.array([0.0, 1.0, 0.0])
a3 = c * np.array([0.0, 0.0, 1.0])
atoms = Atoms([Atom('Ti', [0., 0., 0.]),
               Atom('Ti', 0.5 * a1 + 0.5 * a2 + 0.5 * a3),
               Atom('O', u * a1 + u * a2),
               Atom('O', -u * a1 - u * a2),
               Atom('O', (0.5 + u) * a1 + (0.5 - u) * a2 + 0.5 * a3),
               Atom('O', (0.5 - u) * a1 + (0.5 + u) * a2 + 0.5 * a3)],
              cell=[a1, a2, a3])
KPOINTS = [2, 3, 4, 5, 6, 7, 8]
energies = []
ready = True
for k in KPOINTS:
    with jasp('bulk/tio2/kpts-{0}'.format(k),
              encut=520,
              kpts=(k, k, k),
              xc='PBE',
              sigma=0.05,
              atoms=atoms) as calc:
        try:
            energies.append(atoms.get_potential_energy())
        except (VaspSubmitted, VaspQueued):
            ready = False
if not ready:
    import sys; sys.exit()
plt.plot(KPOINTS, energies)
plt.xlabel('number of k-points in each vector')
plt.ylabel('Total energy (eV)')
plt.savefig('images/tio2-kpt-convergence.png')
plt.show()