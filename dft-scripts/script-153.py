from ase import Atoms, Atom
from vasp import Vasp
import matplotlib.pyplot as plt
import numpy as np
a = 3.9  # approximate lattice constant
b = a / 2.
bulk = Atoms([Atom('Pd', (0.0, 0.0, 0.0))],
             cell=[(0, b, b),
                   (b, 0, b),
                   (b, b, 0)])
RWIGS = [1.0, 1.1, 1.25, 1.5, 2.0, 2.5, 3.0, 4.0, 5.0 ]
ED, WD, N = [], [], []
for rwigs in RWIGS:
    calc = Vasp('bulk/pd-ados')
    calc.clone('bulk/pd-ados-rwigs-{0}'.format(rwigs))
    calc.set(rwigs={'Pd': rwigs})
    if calc.potential_energy is None:
        continue
        # now get results
        ados = VaspDos(efermi=calc.get_fermi_level())
        energies = ados.energy
        dos = ados.site_dos(0, 'd')
        #we will select energies in the range of -10, 5
        ind = (energies < 5) & (energies > -10)
        energies = energies[ind]
        dos = dos[ind]
        Nstates = np.trapz(dos, energies)
        occupied = energies <= 0.0
        N_occupied_states = np.trapz(dos[occupied], energies[occupied])
        ed = np.trapz(energies * dos, energies) / np.trapz(dos, energies)
        wd2 = np.trapz(energies**2 * dos, energies) / np.trapz(dos, energies)
        N.append(N_occupied_states)
        ED.append(ed)
        WD.append(wd2**0.5)
plt.plot(RWIGS, N, 'bo', label='N. occupied states')
plt.legend(loc='best')
plt.xlabel('RWIGS ($\AA$)')
plt.ylabel('# occupied states')
plt.savefig('images/ados-rwigs-occupation.png')
fig, ax1 = plt.subplots()
ax1.plot(RWIGS, ED, 'bo', label='d-band center (eV)')
ax1.set_xlabel('RWIGS ($\AA$)')
ax1.set_ylabel('d-band center (eV)', color='b')
for tl in ax1.get_yticklabels():
    tl.set_color('b')
ax2 = ax1.twinx()
ax2.plot(RWIGS, WD, 'gs', label='d-band width (eV)')
ax2.set_ylabel('d-band width (eV)', color='g')
for tl in ax2.get_yticklabels():
    tl.set_color('g')
plt.savefig('images/ados-rwigs-moments.png')
plt.show()