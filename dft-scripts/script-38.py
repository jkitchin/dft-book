from jasp import *
import numpy as np
import matplotlib.pyplot as plt
np.set_printoptions(precision=3, suppress=True)
bond_lengths = [1.05, 1.1, 1.15, 1.2, 1.25]
energies = []
for d in bond_lengths:  # possible bond lengths
    with jasp('molecules/co-{0}'.format(d)) as calc:
        atoms = calc.get_atoms()
        energies.append(atoms.get_potential_energy())
# Now we fit an equation - cubic polynomial
pp = np.polyfit(bond_lengths, energies, 3)
dp = np.polyder(pp)  # first derivative - quadratic
# we expect two roots from the quadratic eqn. These are where the
# first derivative is equal to zero.
roots = np.roots(dp)
# The minimum is where the second derivative is positive.
dpp = np.polyder(dp)  # second derivative - line
secd = np.polyval(dpp, roots)
minV = roots[secd > 0]
minE = np.polyval(pp, minV)
print 'The minimum energy is {0} eV at V = {1} Ang^3'.format(minE, minV)
# plot the fit
x = np.linspace(1.05, 1.25)
fit = np.polyval(pp, x)
plt.plot(bond_lengths, energies, 'bo ')
plt.plot(x, fit, 'r-')
plt.plot(minV, minE, 'm* ')
plt.legend(['DFT', 'fit', 'minimum'], numpoints=1)
plt.xlabel(r'Bond length ($\AA$)')
plt.ylabel('Total energy (eV)')
plt.savefig('images/co-bondlengths.png')
plt.show()