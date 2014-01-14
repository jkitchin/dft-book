import numpy as np
import matplotlib.pyplot as plt
from ase.units import *
K = 1. #not defined in ase.units!
# Shomate parameters
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
T = np.linspace(100,700)
G = enthalpy(T) - T*entropy(T)
plt.plot(T,G)
plt.xlabel('Temperature (K)')
plt.ylabel('$\Delta G^\circ$ (eV)')
plt.savefig('images/O2-mu.png')