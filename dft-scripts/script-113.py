from vasp import Vasp
factors = [0.9, 0.95, 1.0, 1.05, 1.1]  # to change volume by
energies1, volumes1 = [], []  # from step 1
energies, volumes = [], []  # for step 2
ready = True
for f in factors:
    calc = Vasp('bulk/tio2/step1-{0:1.2f}'.format(f))
    atoms = calc.get_atoms()
    energies1.append(atoms.get_potential_energy())
    volumes1.append(atoms.get_volume())
    calc.clone('bulk/tio2/step2-{0:1.2f}'.format(f))
    calc.set(isif=4)
    # You have to get the atoms again.
    atoms = calc.get_atoms()
    energies.append(atoms.get_potential_energy())
    volumes.append(atoms.get_volume())
print(energies, volumes)
calc.stop_if(None in energies)
import matplotlib.pyplot as plt
plt.plot(volumes1, energies1, volumes, energies)
plt.xlabel('Vol. ($\AA^3)$')
plt.ylabel('Total energy (eV)')
plt.legend(['step 1', 'step 2'], loc='best')
plt.savefig('images/tio2-step2.png')