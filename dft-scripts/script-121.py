from jasp import *
from ase import Atom, Atoms
# fcc
LC = [3.5, 3.55, 3.6, 3.65, 3.7, 3.75]
volumes, energies = [], []
for a in LC:
    atoms = Atoms([Atom('Ni', (0, 0, 0), magmom=2.5)],
              cell=0.5 * a * np.array([[1.0, 1.0, 0.0],
                                       [0.0, 1.0, 1.0],
                                       [1.0, 0.0, 1.0]]))
    with jasp('bulk/Ni-{0}'.format(a),
              xc='PBE',
              encut=350,
              kpts=(12,12,12),
              ispin=2,
              atoms=atoms) as calc:
        try:
            e = atoms.get_potential_energy()
            energies.append(e)
            volumes.append(atoms.get_volume())
        except:
            pass
if len(energies) != len(LC):
    import sys; sys.exit()
import matplotlib.pyplot as plt
plt.plot(LC, fcc_energies)
plt.xlabel('Lattice constant ($\AA$)')
plt.ylabel('Total energy (eV)')
plt.savefig('images/Ni-fcc.png')