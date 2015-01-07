import matplotlib.pyplot as plt
import numpy as np
from ase.units import *
atm = 101325 * Pascal #atm is not defined in units
K = 1 # Kelvin
# examine range over 10^-10 to 10^10 atm
P = np.logspace(-10, 10) * atm
plt.semilogx(P / atm, kB * (300 * K) * np.log(P / (1 * atm)), label='300K')
plt.semilogx(P / atm, kB * (600 * K) * np.log(P / (1 * atm)), label='600K')
plt.xlabel('Pressure (atm)')
plt.ylabel('$\Delta G$ (eV)')
plt.legend(loc='best')
plt.savefig('images/O2-g-p.png')