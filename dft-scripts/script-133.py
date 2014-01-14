from ase import Atoms, Atom
from jasp import *
import sys
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
for k in kpts:
    with jasp('bulk/pd-dos-k{0}-simear-5'.format(k),
              encut=300,
              xc='PBE',
              lreal=False,
              kpts=(k,k,k),
              atoms=bulk) as calc:
        # this runs the calculation
        try:
            bulk.get_potential_energy()
            dos = DOS(calc, width=0.2)
            d = dos.get_dos() + k/4.0
            e = dos.get_energies()
            plt.plot(e,d, label='k={0}'.format(k))
        except:
            pass
plt.xlabel('energy (eV)')
plt.ylabel('DOS')
plt.legend()
plt.savefig('images/pd-dos-k-convergence-ismear-5.png')
plt.show()