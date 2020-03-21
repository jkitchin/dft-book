from scipy.optimize import leastsq
import numpy as np
vols = np.array([13.71, 14.82, 16.0, 17.23, 18.52])
energies = np.array([-56.29, -56.41, -56.46, -56.463, -56.41])
def Murnaghan(parameters, vol):
    'From Phys. Rev. B 28, 5480 (1983)'
    E0 = parameters[0]
    B0 = parameters[1]
    BP = parameters[2]
    V0 = parameters[3]
    E = (E0 + B0*vol / BP*(((V0 / vol)**BP) / (BP - 1) + 1)
         - V0 * B0 / (BP - 1.))
    return E
def objective(pars, y, x):
    # we will minimize this function
    err = y - Murnaghan(pars, x)
    return err
x0 = [-56., 0.54, 2., 16.5]  # initial guess of parameters
plsq = leastsq(objective, x0, args=(energies, vols))
print('Fitted parameters = {0}'.format(plsq[0]))
import matplotlib.pyplot as plt
plt.plot(vols, energies, 'ro')
# plot the fitted curve on top
x = np.linspace(min(vols), max(vols), 50)
y = Murnaghan(plsq[0], x)
plt.plot(x, y, 'k-')
plt.xlabel('Volume')
plt.ylabel('energy')
plt.savefig('images/nonlinear-curve-fitting.png')