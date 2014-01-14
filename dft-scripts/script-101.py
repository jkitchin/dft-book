from jasp import *
factors = [0.9, 0.95, 1.0, 1.05, 1.1] #to change volume by
energies1, volumes1 = [], [] # from step 1
energies, volumes = [], [] # for step 2
ready = True
for f in factors:
    with jasp('bulk/tio2/step1-{0:1.2f}'.format(f)) as calc:
        atoms = calc.get_atoms()
        energies1.append(atoms.get_potential_energy())
        volumes1.append(atoms.get_volume())
        calc.clone('bulk/tio2/step2-{0:1.2f}'.format(f))
    # now set ISIF=4 and run
    with jasp('bulk/tio2/step2-{0:1.2f}'.format(f),
              isif=4) as calc:
        atoms = calc.get_atoms()
        try:
            energies.append(atoms.get_potential_energy())
            volumes.append(atoms.get_volume())
        except (VaspSubmitted, VaspQueued):
            ready = False
if not ready:
    import sys; sys.exit()
import matplotlib.pyplot as plt
plt.plot(volumes1, energies1, volumes, energies)
plt.xlabel('Vol. ($\AA^3)$')
plt.ylabel('Total energy (eV)')
plt.legend(['step 1', 'step 2'], loc='best')
plt.savefig('images/tio2-step2.png')
plt.show()