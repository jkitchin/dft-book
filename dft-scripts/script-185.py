import numpy as np
import matplotlib.pyplot as plt
from ase.units import *
from scipy.optimize import fsolve
K = 1. #not defined in ase.units!
atm = 101325*Pascal
# Shomate parameters valid from 100-700K
A = 31.32234; B = -20.23531; C = 57.86644
D = -36.50624; E = -0.007374; F = -8.903471
G = 246.7945; H = 0.0
def entropy(T):
    '''entropy returned as eV/K
    T in K
    '''
    t = T/1000.
    s = A*np.log(t) + B*t + C*(t**2)/2. + D*(t**3)/3. - E/(2.*t**2) + G
    return s*J/mol/K
def enthalpy(T):
    ''' H - H(298.15) returned as eV/molecule'''
    t = T/1000.
    h = A*t + B*(t**2)/2. + C*(t**3)/3. + D*(t**4)/4. - E/t + F - H
    return h*kJ/mol
def DeltaMu(T,P):
    '''
    T in K
    P in atm
    '''
    return enthalpy(T) - T*entropy(T) + kB*T*np.log(P/atm)
P = np.logspace(-11,1,10)*atm
T = []
for p in P:
    def func(T):
        return -0.99 - 0.5*DeltaMu(T,p)
    T.append(fsolve(func, 450)[0])
plt.semilogy(T,P/atm)
plt.xlabel('Temperature (K)')
plt.ylabel('Pressure (atm)')
plt.text(800,1e-7,'Ag')
plt.text(600,1e-3,'Ag$_2$O')
plt.savefig('images/Ag2O-decomposition.png')