from vasp import Vasp
from ase import Atom, Atoms
import matplotlib.pyplot as plt
import numpy as np
a = 3.61
atoms = Atoms([Atom('Cu', (0, 0, 0))],
              cell=0.5 * a * np.array([[1.0, 1.0, 0.0],
                                       [0.0, 1.0, 1.0],
                                       [1.0, 0.0, 1.0]])).repeat((2, 2, 2))
SIGMA = [0.001, 0.05, 0.1, 0.2, 0.5]
for sigma in SIGMA:
    calc = Vasp('bulk/Cu-sigma-{0}'.format(sigma),
                xc='PBE',
                encut=350,
                kpts=[4, 4, 4],
                ismear=-1,
                sigma=sigma,
                nbands=9 * 8,
                atoms=atoms)
    if calc.potential_energy is not None:
        nbands = calc.parameters.nbands
        nkpts = len(calc.get_ibz_k_points())
        occ = np.zeros((nkpts, nbands))
        for i in range(nkpts):
            occ[i, :] = calc.get_occupation_numbers(kpt=i)
        max_occ = np.max(occ, axis=0) #axis 0 is columns
        plt.plot(range(nbands), max_occ, label='$\sigma = {0}$'.format(sigma))
plt.xlabel('band number')
plt.ylabel('maximum occupancy (electrons)')
plt.ylim([-0.1, 2.1])
plt.legend(loc='best')
plt.savefig('images/occ-sigma.png')