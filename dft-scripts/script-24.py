from ase.units import kB, Pascal
import numpy as np
import matplotlib.pyplot as plt
atm = 101325 * Pascal
L = np.linspace(4, 10)
V = L**3
n = 1  # one atom/molecule per unit cell
for T in [298, 600, 1000]:
    P = n / V * kB * T / atm  # convert to atmospheres
    plt.plot(V, P, label='{0}K'.format(T))
plt.xlabel('Unit cell volume ($\AA^3$)')
plt.ylabel('Pressure (atm)')
plt.legend(loc='best')
plt.savefig('images/ideal-gas-pressure.png')