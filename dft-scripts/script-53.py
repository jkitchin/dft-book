from ase.structure import molecule
from ase.thermochemistry import IdealGasThermo
from jasp import *
atoms = molecule('N2')
atoms.set_cell((10,10,10), scale_atoms=False)
# first we relax a molecule
with jasp('molecules/n2-relax',
          xc='PBE',
          encut=300,
          ibrion=2,
          nsw=5,
          atoms=atoms) as calc:
    electronicenergy = atoms.get_potential_energy()
# next, we get vibrational modes
with jasp('molecules/n2-vib',
          xc='PBE',
          encut=300,
          ibrion=6,
          nfree=2,
          potim=0.15,
          nsw=1,
          atoms=atoms) as calc:
    calc.calculate()
    vib_freq = calc.get_vibrational_frequencies() # in cm^1
    #convert wavenumbers to energy
    h = 4.1356675e-15 # eV*s
    c = 3.0e10 #cm/s
    vib_energies = [h*c*nu for nu in vib_freq]
    print('vibrational energies\n====================')
    for i,e in enumerate(vib_energies):
        print('{0:02d}: {1} eV'.format(i,e))
# # now we can get some properties. Note we only need one vibrational
# energy since there is only one mode. This example does not work if
# you give all the energies because one energy is zero.
thermo = IdealGasThermo(vib_energies=vib_energies[0:0],
                        electronicenergy=electronicenergy, atoms=atoms,
                        geometry='linear', symmetrynumber=2, spin=0)
# temperature in K, pressure in Pa, G in eV
G = thermo.get_free_energy(temperature=298.15, pressure=101325.)