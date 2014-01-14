import numpy as np
import matplotlib.pyplot as plt
fcc25 = -1.04
hcp25 = -0.60
bridge25 = -0.49
fcc1 = -0.10
Dmu = np.linspace(-4,0)
plt.plot(Dmu, np.zeros(Dmu.shape), label='Pt(111)')
plt.plot(Dmu, fcc25 - 0.5*Dmu, label='fcc - 0.25 ML')
plt.plot(Dmu, hcp25 - 0.5*Dmu, label='hcp - 0.25 ML')
plt.plot(Dmu, bridge25 - 0.5*Dmu, label='bridge - 0.25 ML')
plt.plot(Dmu, fcc1 - 0.5*Dmu, label='fcc - 1.0 ML')
plt.xlabel('$\Delta \mu O_2$ (eV)')
plt.ylabel('$\Delta G_{ads}$ (eV/O)')
plt.legend(loc='best')
plt.savefig('images/atomistic-thermo-adsorption.png')