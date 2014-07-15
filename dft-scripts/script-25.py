from ase import Atoms,Atom
from jasp import *
import numpy as np
np.set_printoptions(precision=3, suppress=True)
atoms = Atoms([Atom('C',[0,   0, 0]),
               Atom('O',[1.2, 0, 0])],
               cell=(6,6,6))
atoms.center()
ENCUTS = [250, 300, 350, 400, 450, 500]
energies = []
ready = True
for en in ENCUTS:
    with jasp('molecules/co-en-{0}'.format(en),
              encut=en,
              xc='PBE',
              atoms=atoms) as calc:
        try:
            energies.append(atoms.get_potential_energy())
        except (VaspSubmitted, VaspQueued):
            ready = False
if not ready:
   import sys; sys.exit()
import matplotlib.pyplot as plt
plt.plot(ENCUTS, energies, 'bo-')
plt.xlabel('ENCUT (eV)')
plt.ylabel('Total energy (eV)')
plt.savefig('images/co-encut-v.png')