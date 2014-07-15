from jasp import *
from ase.units import *
bond_lengths = [1.05, 1.1, 1.15, 1.2, 1.25]
energies = []
for d in bond_lengths:
    with jasp('molecules/co-{0}'.format(d)) as calc:
        atoms = calc.get_atoms()
        energies.append(atoms.get_potential_energy())
# fit the data
pars = np.polyfit(bond_lengths, energies, 3)
xfit = np.linspace(1.05, 1.25)
efit = np.polyval(pars, xfit)
# first derivative
dpars = np.polyder(pars)
# find where the minimum is. chose the second one because it is the
# minimum we need.
droots = np.roots(dpars)
# second derivative
ddpars = np.polyder(dpars)
d_min = droots[np.polyval(ddpars, droots) > 0]
#curvature at minimum = force constant in SI units
k = np.polyval(ddpars, d_min) / (J / m**2)
# mu, reduced mass
from ase.data import atomic_masses
C_mass = atomic_masses[6] / kg
O_mass = atomic_masses[8] / kg
mu = 1.0 / (1.0 / C_mass + 1.0 / O_mass)
frequency = 1. / (2. * np.pi) * np.sqrt(k / mu)
print 'The CO vibrational frequency is {0} Hz'.format(*frequency)
print 'The CO vibrational frequency is {0} cm^{{-1}}'.format(frequency/3e10)
import matplotlib.pyplot as plt
plt.plot(bond_lengths, energies, 'bo ')
plt.plot(xfit, efit, 'b-')
plt.xlabel('Bond length ($\AA$)')
plt.ylabel('Total energy (eV)')
plt.show()