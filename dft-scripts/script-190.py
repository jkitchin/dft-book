import numpy as np
import matplotlib.pyplot as plt
fcc25 = -1.04
hcp25 = -0.60
bridge25 = -0.49
fcc1 = -0.10
Dmu = np.linspace(-4,2)
plt.plot(Dmu, np.zeros(Dmu.shape), label='Pt(111)')
plt.plot(Dmu, 0.25 * (fcc25 - 0.5*Dmu), label='fcc - 0.25 ML')
plt.plot(Dmu, 0.25 * (hcp25 - 0.5*Dmu), label='hcp - 0.25 ML')
plt.plot(Dmu, 0.25 * (bridge25 - 0.5*Dmu), label='bridge - 0.25 ML')
plt.plot(Dmu, 1.0 * (fcc1 - 0.5*Dmu), label='fcc - 1.0 ML')
plt.xlabel('$\Delta \mu O_2$ (eV)')
plt.ylabel('$\Delta G_{ads}$ (eV/O)')
plt.legend(loc='best')
plt.savefig('images/atomistic-thermo-adsorption.png')
plt.show()