from ase import Atoms, Atom
from jasp import *
import sys
import matplotlib.pyplot as plt
import numpy as np
from ase.dft import DOS
a = 3.9  # approximate lattice constant
b = a / 2.
bulk = Atoms([Atom('Pd', (0.0, 0.0, 0.0))],
             cell=[(0, b, b),
                   (b, 0, b),
                   (b, b, 0)])
with jasp('bulk/pd-dos',
          encut=300,
          xc='PBE',
          lreal=False,
          kpts=(8, 8, 8),  # this is too low for high quality DOS
          atoms=bulk) as calc:
    # this runs the calculation
    bulk.get_potential_energy()
    dos = DOS(calc, width=0.2)
    d = dos.get_dos()
    e = dos.get_energies()
import pylab as plt
plt.plot(e,d)
plt.xlabel('energy (eV)')
plt.ylabel('DOS')
plt.savefig('images/pd-dos.png')