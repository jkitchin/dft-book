import numpy as np
import matplotlib.pyplot as plt
from ase.units import *
from scipy.optimize import fsolve
K = 1. #not defined in ase.units!
atm = 101325 * Pascal
# Shomate parameters valid from 100-700K
A = 31.32234; B = -20.23531; C = 57.86644
D = -36.50624; E = -0.007374; F = -8.903471
G = 246.7945; H = 0.0
def entropy(T):
    '''entropy returned as eV/K
    T in K
    '''
    t = T/1000.
    s = A * np.log(t) + B * t + C * (t**2) / 2. + D * (t**3) / 3. - E / (2. * t**2) + G
    return s * J / mol / K
def enthalpy(T):
    ''' H - H(298.15) returned as eV/molecule'''
    t = T / 1000.
    h = A * t + B * (t**2) / 2. + C * (t**3) / 3. + D * (t**4) / 4. - E / t + F - H
    return h * kJ / mol
def DeltaMu(T, P):
    '''
    returns delta chemical potential of oxygen at T and P
    T in K
    P in atm
    '''
    return enthalpy(T) - T * entropy(T) + kB * T * np.log(P / atm)
P = 1e-10*atm
def func(T):
    'Cu2O'
    return -1.95 - 0.5*DeltaMu(T, P)
print 'Cu2O decomposition temperature is {0:1.0f} K'.format(fsolve(func, 900)[0])
def func(T):
    'Ag2O'
    return -0.99 - 0.5 * DeltaMu(T, P)
print 'Ag2O decomposition temperature is {0:1.0f} K'.format(fsolve(func, 470)[0])
T = np.linspace(100, 1000)
# Here we plot delta mu as a function of temperature at different pressures
# you have use \\times to escape the first \ in pyplot
plt.plot(T, DeltaMu(T, 1e10*atm), label='1$\\times 10^{10}$ atm')
plt.plot(T, DeltaMu(T, 1e5*atm), label='1$\\times 10^5$ atm')
plt.plot(T, DeltaMu(T, 1*atm), label='1 atm')
plt.plot(T, DeltaMu(T, 1e-5*atm), label='1$\\times 10^{-5}$ atm')
plt.plot(T, DeltaMu(T, 1e-10*atm), label='1$\\times 10^{-10}$ atm')
plt.xlabel('Temperature (K)')
plt.ylabel('$\Delta \mu_{O_2}(T,p)$ (eV)')
plt.legend(loc='best')
plt.savefig('images/O2-mu-diff-p.png')