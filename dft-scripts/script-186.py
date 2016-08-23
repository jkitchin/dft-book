from vasp import Vasp
from ase.lattice.surface import fcc111
import matplotlib.pyplot as plt
Nlayers = [3, 4, 5, 6, 7, 8, 9, 10, 11]
energies = []
sigmas = []
for n in Nlayers:
    slab = fcc111('Cu', size=(1, 1, n), vacuum=10.0)
    slab.center()
    calc = Vasp('bulk/Cu-layers/{0}'.format(n),
                xc='PBE',
                encut=350,
                kpts=[8, 8, 1],
                atoms=slab)
    calc.set_nbands(f=2)  # the default nbands in VASP is too low for Cu
    energies.append(slab.get_potential_energy())
calc.stop_if(None in energies)
for i in range(len(Nlayers) - 1):
    N = Nlayers[i]
    DeltaE_N = energies[i + 1] - energies[i]
    sigma = 0.5 * (-N * energies[i + 1] + (N + 1) * energies[i])
    sigmas.append(sigma)
    print 'nlayers = {1:2d} sigma = {0:1.3f} eV/atom'.format(sigma, N)
plt.plot(Nlayers[0:-1], sigmas, 'bo-')
plt.xlabel('Number of layers')
plt.ylabel('Surface energy (eV/atom)')
plt.savefig('images/Cu-unrelaxed-surface-energy.png')