from ase.thermochemistry import IdealGasThermo
from vasp import Vasp
import numpy as np
import matplotlib.pyplot as plt
# first we get the electronic energies
c1 = Vasp('molecules/wgs/CO')
E_CO = c1.potential_energy
CO = c1.get_atoms()
c2 = Vasp('molecules/wgs/CO2')
E_CO2 = c2.potential_energy
CO2 = c2.get_atoms()
c3 = Vasp('molecules/wgs/H2')
E_H2 = c3.potential_energy
H2 = c3.get_atoms()
c4 = Vasp('molecules/wgs/H2O')
E_H2O = c4.potential_energy
H2O = c4.get_atoms()
# now we get the vibrational energies
h = 4.1356675e-15  # eV * s
c = 3.0e10  # cm / s
calc = Vasp('molecules/wgs/CO-vib')
vib_freq = calc.get_vibrational_frequencies()
CO_vib_energies = [h * c * nu for nu in vib_freq]
calc = Vasp('molecules/wgs/CO2-vib')
vib_freq = calc.get_vibrational_frequencies()
CO2_vib_energies = [h * c * nu for nu in vib_freq]
calc = Vasp('molecules/wgs/H2-vib')
vib_freq = calc.get_vibrational_frequencies()
H2_vib_energies = [h * c * nu for nu in vib_freq]
calc = Vasp('molecules/wgs/H2O-vib')
vib_freq = calc.get_vibrational_frequencies()
H2O_vib_energies = [h * c * nu for nu in vib_freq]
# now we make a thermo object for each molecule
CO_t = IdealGasThermo(vib_energies=CO_vib_energies[0:0],
                      potentialenergy=E_CO, atoms=CO,
                      geometry='linear', symmetrynumber=1,
                      spin=0)
CO2_t = IdealGasThermo(vib_energies=CO2_vib_energies[0:4],
                      potentialenergy=E_CO2, atoms=CO2,
                      geometry='linear', symmetrynumber=2,
                      spin=0)
H2_t = IdealGasThermo(vib_energies=H2_vib_energies[0:0],
                      potentialenergy=E_H2, atoms=H2,
                      geometry='linear', symmetrynumber=2,
                      spin=0)
H2O_t = IdealGasThermo(vib_energies=H2O_vib_energies[0:3],
                      potentialenergy=E_H2O, atoms=H2O,
                      geometry='nonlinear', symmetrynumber=2,
                      spin=0)
# now we can compute G_rxn for a range of temperatures from 298 to 1000 K
Trange = np.linspace(298, 1000, 20)  # K
P = 101325. # Pa
Grxn = np.array([(CO2_t.get_gibbs_energy(temperature=T, pressure=P)
                  + H2_t.get_gibbs_energy(temperature=T, pressure=P)
                  - H2O_t.get_gibbs_energy(temperature=T, pressure=P)
                  - CO_t.get_gibbs_energy(temperature=T, pressure=P)) * 96.485
                 for T in Trange])
Hrxn = np.array([(CO2_t.get_enthalpy(temperature=T)
                  + H2_t.get_enthalpy(temperature=T)
                  - H2O_t.get_enthalpy(temperature=T)
                  - CO_t.get_enthalpy(temperature=T)) * 96.485
                 for T in Trange])
plt.plot(Trange, Grxn, 'bo-', label='$\Delta G_{rxn}$')
plt.plot(Trange, Hrxn, 'ro:', label='$\Delta H_{rxn}$')
plt.xlabel('Temperature (K)')
plt.ylabel(r'$\Delta G_{rxn}$ (kJ/mol)')
plt.legend(loc='best')
plt.savefig('images/wgs-dG-T.png')
plt.figure()
R = 8.314e-3  # gas constant in kJ/mol/K
Keq = np.exp(-Grxn/R/Trange)
plt.plot(Trange, Keq)
plt.ylim([0, 100])
plt.xlabel('Temperature (K)')
plt.ylabel('$K_{eq}$')
plt.savefig('images/wgs-Keq.png')