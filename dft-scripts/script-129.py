from vasp import Vasp
from ase.lattice.cubic import FaceCenteredCubic
import numpy as np
import matplotlib.pyplot as plt
DELTAS = np.linspace(-0.05, 0.05, 5)
calcs = []
volumes = []
for delta in DELTAS:
    atoms = FaceCenteredCubic(symbol='Al')
    cell = atoms.cell
    T = np.array([[1 + delta, 0, 0],
                  [0,1, 0],
                  [0, 0, 1]])
    newcell = np.dot(cell, T)
    atoms.set_cell(newcell, scale_atoms=True)
    volumes += [atoms.get_volume()]
    calcs += [Vasp('bulk/Al-c11-{}'.format(delta),
                xc='pbe',
                kpts=[12, 12, 12],
                encut=350,
                atoms=atoms)]
Vasp.run()
energies =  [calc.potential_energy for calc in calcs]
# fit a parabola
eos = np.polyfit(DELTAS, energies, 2)
# first derivative
d_eos = np.polyder(eos)
print(np.roots(d_eos))
xfit = np.linspace(min(DELTAS), max(DELTAS))
yfit = np.polyval(eos, xfit)
plt.plot(DELTAS, energies, 'bo', xfit, yfit, 'b-')
plt.xlabel('$\delta$')
plt.ylabel('Energy (eV)')
plt.savefig('images/Al-c11.png')