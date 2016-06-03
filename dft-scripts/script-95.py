from ase.lattice.cubic import FaceCenteredCubic
from vasp import Vasp
import numpy as np
atoms = FaceCenteredCubic('Ag')
KPTS = [2, 3, 4, 5, 6, 8, 10]
TE = []
for k in KPTS:
    calc = Vasp('bulk/Ag-kpts-{0}'.format(k),
                xc='PBE',
                kpts=[k, k, k],  # specifies the Monkhorst-Pack grid
                encut=300,
                atoms=atoms)
    TE.append(atoms.get_potential_energy())
if None in TE:
    calc.abort()
import matplotlib.pyplot as plt
# consider the change in energy from lowest energy state
TE = np.array(TE)
TE -= TE.min()
plt.plot(KPTS, TE)
plt.xlabel('number of k-points in each dimension')
plt.ylabel('Total Energy (eV)')
plt.savefig('images/Ag-kpt-convergence.png')