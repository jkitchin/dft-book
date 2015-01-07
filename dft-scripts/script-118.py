# fit cubic polynomials to E(V) for rutile and anatase
from jasp import *
import matplotlib.pyplot as plt
import numpy as np
np.set_printoptions(precision=2)
# anatase equation of state
volumes = [30., 33., 35., 37., 39.]  # vol of one TiO2 formula unit
a_volumes, a_energies = [], []
for v in volumes:
    with jasp('bulk/TiO2/anatase/anatase-{0}'.format(v)) as calc:
        atoms = calc.get_atoms()
        nTiO2 = len(atoms) / 3.0
        a_volumes.append(atoms.get_volume() / nTiO2)
        a_energies.append(atoms.get_potential_energy() / nTiO2)
# rutile equation of state
volumes = [28., 30., 32., 34., 36.]  # vol of one TiO2
r_volumes, r_energies = [], []
for v in volumes:
    with jasp('bulk/TiO2/rutile/rutile-{0}'.format(v)) as calc:
        atoms = calc.get_atoms()
        nTiO2 = len(atoms) / 3.0
        r_volumes.append(atoms.get_volume() / nTiO2)
        r_energies.append(atoms.get_potential_energy() / nTiO2)
# cubic polynomial fit to equation of state E(V) = pars*[V^3 V^2 V^1 V^0]
apars = np.polyfit(a_volumes, a_energies, 3)
rpars = np.polyfit(r_volumes, r_energies, 3)
print 'E_anatase(V) = {0:1.2f}*V^3 + {1:1.2f}*V^2 + {2:1.2f}*V + {3:1.2f}'.format(*apars)
print 'E_rutile(V) =  {0:1.2f}*V^3 + {1:1.2f}*V^2 + {2:1.2f}*V + {3:1.2f}'.format(*rpars)
print 'anatase epars: {0!r}'.format(apars)
print 'rutile epars: {0!r}'.format(rpars)
# get pressure parameters P(V) = -dE/dV
dapars = -np.polyder(apars)
drpars = -np.polyder(rpars)
print 'anatase ppars: {0!r}'.format(dapars)
print 'rutile ppars: {0!r}'.format(drpars)
print
print 'P_anatase(V) = {0:1.2f}*V^2 + {1:1.2f}*V + {2:1.2f}'.format(*dapars)
print 'P_rutile(V) =  {0:1.2f}*V^2 + {1:1.2f}*V + {2:1.2f}'.format(*drpars)
vfit = np.linspace(28, 40)
# plot the equations of state
plt.plot(a_volumes, a_energies,'bo ', label='Anatase')
plt.plot(vfit, np.polyval(apars, vfit), 'b-')
plt.plot(r_volumes, r_energies,'gs ', label='Rutile')
plt.plot(vfit, np.polyval(rpars, vfit), 'g-')
plt.xlabel('Volume ($\AA^3$/f.u.)')
plt.ylabel('Total energy (eV/f.u.)')
plt.legend()
plt.xlim([25, 40])
plt.ylim([-27, -26])
plt.savefig('images/rutile-anatase-eos.png')