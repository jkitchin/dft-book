import numpy as np
import matplotlib.pyplot as plt
from ase.units import *
K = 1.  # not defined in ase.units!
atm = 101325*Pascal
Hf = -0.99
P = 1 * atm
Dmu = np.linspace(-4, 0)
Hf = -0.99 - 0.5*Dmu
plt.plot(Dmu, Hf, label='Ag$_2$O')
plt.plot(Dmu, np.zeros(Hf.shape), label='Ag')
plt.xlabel(r'$\Delta \mu_{O_2}$ (eV)')
plt.ylabel('$H_f$ (eV)')
plt.savefig('images/atomistic-thermo-hf-mu.png')