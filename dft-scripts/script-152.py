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
calc = Vasp('bulk/pd-ados',
            encut=300,
            xc='PBE',
            lreal=False,
            rwigs={'Pd': 1.5},  # wigner-seitz radii for ados
            kpts=[8, 8, 8],
            atoms=bulk)
# this runs the calculation
calc.wait(abort=True)
# now get results
energies, ados = calc.get_ados(0, 'd')
# we will select energies in the range of -10, 5
ind = (energies < 5) & (energies > -10)
energies = energies[ind]
dos = ados[ind]
Nstates = np.trapz(dos, energies)
occupied = energies <= 0.0
N_occupied_states = np.trapz(dos[occupied], energies[occupied])
# first moment
ed = np.trapz(energies * dos, energies) / Nstates
# second moment
wd2 = np.trapz(energies**2 * dos, energies) / Nstates
print 'Total # states = {0:1.2f}'.format(Nstates)
print 'number of occupied states = {0:1.2f}'.format(N_occupied_states)
print 'd-band center = {0:1.2f} eV'.format(ed)
print 'd-band width  = {0:1.2f} eV'.format(np.sqrt(wd2))
# plot the d-band
plt.plot(energies, dos, label='$d$-orbitals')
# plot the occupied states in shaded gray
plt.fill_between(x=energies[occupied],
                 y1=dos[occupied],
                 y2=np.zeros(dos[occupied].shape),
                 color='gray', alpha=0.25)
plt.xlabel('$E - E_f$ (eV)')
plt.ylabel('DOS (arbitrary units)')
plt.savefig('images/pd-ados.png')