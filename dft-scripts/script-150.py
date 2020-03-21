from ase import Atoms, Atom
from vasp import Vasp
Vasp.vasprc(mode=None)
#Vasp.log.setLevel(10)
import matplotlib.pyplot as plt
import numpy as np
from ase.dft import DOS
import pylab as plt
a = 3.9  # approximate lattice constant
b = a / 2.
bulk = Atoms([Atom('Pd', (0.0, 0.0, 0.0))],
             cell=[(0, b, b),
                   (b, 0, b),
                   (b, b, 0)])
kpts = [8, 10, 12, 14, 16, 18, 20]
calcs = [Vasp('bulk/pd-dos-k{0}-ismear-5'.format(k),
              encut=300,
              xc='PBE',
              kpts=[k, k, k],
              atoms=bulk) for k in kpts]
Vasp.wait(abort=True)
for calc in calcs:
    # this runs the calculation
    if calc.potential_energy is not None:
        dos = DOS(calc, width=0.2)
        d = dos.get_dos() + k / 4.0
        e = dos.get_energies()
        plt.plot(e, d, label='k={0}'.format(k))
    else:
        pass
plt.xlabel('energy (eV)')
plt.ylabel('DOS')
plt.legend()
plt.savefig('images/pd-dos-k-convergence-ismear-5.png')
plt.show()