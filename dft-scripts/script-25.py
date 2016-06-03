from ase import Atoms, Atom
from vasp import Vasp
import numpy as np
np.set_printoptions(precision=3, suppress=True)
atoms = Atoms([Atom('C', [0, 0, 0]),
               Atom('O', [1.2, 0, 0])],
              cell=(6, 6, 6))
atoms.center()
ENCUTS = [250, 300, 350, 400, 450, 500]
calcs = [Vasp('molecules/co-en-{0}'.format(en),
              encut=en,
              xc='PBE',
              atoms=atoms)
         for en in ENCUTS]
energies = [calc.potential_energy for calc in calcs]
print(energies)
calcs[0].stop_if(None in energies)
import matplotlib.pyplot as plt
plt.plot(ENCUTS, energies, 'bo-')
plt.xlabel('ENCUT (eV)')
plt.ylabel('Total energy (eV)')
plt.savefig('images/co-encut-v.png')