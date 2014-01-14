from ase.lattice.cubic import FaceCenteredCubic
from jasp import *
atoms = FaceCenteredCubic('Ag')
KPTS = [2, 3, 4, 5, 6, 8, 10]
TE = []
ready = True
for k in KPTS:
    with jasp('bulk/Ag-kpts-{0}'.format(k),
              xc='PBE',
              kpts=(k, k, k), #specifies the Monkhorst-Pack grid
              encut=300,
              atoms=atoms) as calc:
        try:
            TE.append(atoms.get_potential_energy())
        except (VaspSubmitted, VaspQueued):
            ready = False
if not ready:
    import sys; sys.exit()
import matplotlib.pyplot as plt
# consider the change in energy from lowest energy state
TE = np.array(TE)
TE -= TE.min()
plt.plot(KPTS, TE)
plt.xlabel('number of k-points in each dimension')
plt.ylabel('Total Energy (eV)')
plt.savefig('images/Ag-kpt-convergence.png')
plt.show()