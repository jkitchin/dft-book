from ase.thermochemistry import IdealGasThermo
from jasp import *
import numpy as np
import matplotlib.pyplot as plt
# first we get the electronic energies
with jasp('molecules/wgs/CO') as calc:
    CO = calc.get_atoms()
    E_CO = CO.get_potential_energy()
with jasp('molecules/wgs/CO2') as calc:
    CO2 = calc.get_atoms()
    E_CO2 = CO2.get_potential_energy()
with jasp('molecules/wgs/H2') as calc:
    H2 = calc.get_atoms()
    E_H2 = H2.get_potential_energy()
with jasp('molecules/wgs/H2O') as calc:
    H2O = calc.get_atoms()
    E_H2O = H2O.get_potential_energy()
# now we get the vibrational energies
h = 4.1356675e-15 # eV*s
c = 3.0e10 #cm/s
with jasp('molecules/wgs/CO-vib') as calc:
    vib_freq = calc.get_vibrational_frequencies()
    CO_vib_energies = [h*c*nu for nu in vib_freq]
with jasp('molecules/wgs/CO2-vib') as calc:
    vib_freq = calc.get_vibrational_frequencies()
    CO2_vib_energies = [h*c*nu for nu in vib_freq]
with jasp('molecules/wgs/H2-vib') as calc:
    vib_freq = calc.get_vibrational_frequencies()
    H2_vib_energies = [h*c*nu for nu in vib_freq]
with jasp('molecules/wgs/H2O-vib') as calc:
    vib_freq = calc.get_vibrational_frequencies()
    H2O_vib_energies = [h*c*nu for nu in vib_freq]
# now we make a thermo object for each molecule
CO_t = IdealGasThermo(vib_energies=CO_vib_energies[0:0],
                      electronicenergy=E_CO, atoms=CO,
                      geometry='linear', symmetrynumber=1,
                      spin=0)
CO2_t = IdealGasThermo(vib_energies=CO2_vib_energies[0:4],
                      electronicenergy=E_CO2, atoms=CO2,
                      geometry='linear', symmetrynumber=2,
                      spin=0)
H2_t = IdealGasThermo(vib_energies=H2_vib_energies[0:0],
                      electronicenergy=E_H2, atoms=H2,
                      geometry='linear', symmetrynumber=2,
                      spin=0)
H2O_t = IdealGasThermo(vib_energies=H2O_vib_energies[0:3],
                      electronicenergy=E_H2O, atoms=H2O,
                      geometry='nonlinear', symmetrynumber=2,
                      spin=0)
# now we can compute G_rxn for a range of temperatures from 298 to 1000 K
Trange = np.linspace(298,1000,20) #K
P = 101325. # Pa
Grxn = np.array([(CO2_t.get_free_energy(temperature=T, pressure=P)
                  + H2_t.get_free_energy(temperature=T, pressure=P)
                  - H2O_t.get_free_energy(temperature=T, pressure=P)
                  - CO_t.get_free_energy(temperature=T, pressure=P))*96.485 for T in Trange])
Hrxn = np.array([(CO2_t.get_enthalpy(temperature=T)
                  + H2_t.get_enthalpy(temperature=T)
                  - H2O_t.get_enthalpy(temperature=T)
                  - CO_t.get_enthalpy(temperature=T))*96.485 for T in Trange])
plt.plot(Trange, Grxn, 'bo-',label='$\Delta G_{rxn}$')
plt.plot(Trange, Hrxn, 'ro:',label='$\Delta H_{rxn}$')
plt.xlabel('Temperature (K)')
plt.ylabel('$\Delta G_{rxn}$ (kJ/mol)')
plt.legend(loc='best')
plt.savefig('images/wgs-dG-T.png')
plt.figure()
R = 8.314e-3 # gas constant in kJ/mol/K
Keq = np.exp(-Grxn/R/Trange)
plt.plot(Trange, Keq)
plt.ylim([0, 100])
plt.xlabel('Temperature (K)')
plt.ylabel('$K_{eq}$')
plt.savefig('images/wgs-Keq.png')
plt.show()