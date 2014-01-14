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
print 'roots of first derivative are {0}'.format(np.roots(dpars))
d_min = 1.14425395 # we manually copy this from the output to here
# second derivative
ddpars = np.polyder(dpars)
#curvature at minimum = force constant
k = np.polyval(ddpars, d_min) / kg * s**2
# reduced mass
from ase.data import atomic_masses
C_mass = atomic_masses[6] / kg
O_mass = atomic_masses[8] / kg
mu = (C_mass*O_mass)/(C_mass + O_mass)
frequency = 1. / (2. * np.pi) * np.sqrt(k / mu)
print 'The CO vibrational frequency is {0} cm^{{-1}}'.format(frequency/3e10)
import matplotlib.pyplot as plt
plt.plot(bond_lengths, energies, 'bo ')
plt.plot(xfit, efit, 'b-')
plt.xlabel('Bond length ($\AA$)')
plt.ylabel('Total energy (eV)')
plt.show()