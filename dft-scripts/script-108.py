from vasp import Vasp
import matplotlib.pyplot as plt
import numpy as np
x = [2.5, 2.6, 2.7, 2.8, 2.9]
y = [1.4, 1.5, 1.6, 1.7, 1.8]
X,Y = np.meshgrid(x, y)
Z = np.zeros(X.shape)
for i,a in enumerate(x):
    for j,covera in enumerate(y):
        wd = 'bulk/Ru/{0:1.2f}-{1:1.2f}'.format(a, covera)
        calc = Vasp(wd)
        Z[i][j] = calc.potential_energy
calc.stop_if(None in Z)
cf = plt.contourf(X, Y, Z, 20,
                  cmap=plt.cm.jet)
cbar = plt.colorbar(cf)
cbar.ax.set_ylabel('Energy (eV)')
plt.xlabel('$a$ ($\AA$)')
plt.ylabel('$c/a$')
plt.legend()
plt.savefig('images/ru-contourf.png')
plt.show()