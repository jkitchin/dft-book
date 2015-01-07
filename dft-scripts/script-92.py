from jasp import *
from ase import Atom, Atoms
# fcc
LC = [3.5, 3.55, 3.6, 3.65, 3.7, 3.75]
fcc_energies = []
ready = True
for a in LC:
    atoms = Atoms([Atom('Cu', (0, 0, 0))],
              cell=0.5 * a * np.array([[1.0, 1.0, 0.0],
                                       [0.0, 1.0, 1.0],
                                       [1.0, 0.0, 1.0]]))
    with jasp('bulk/Cu-{0}'.format(a),
              xc='PBE',
              encut=350,
              kpts=(8, 8, 8),
              atoms=atoms) as calc:
        try:
            e = atoms.get_potential_energy()
            fcc_energies.append(e)
        except (VaspSubmitted, VaspQueued):
            ready = False
if not ready:
    import sys; sys.exit()
import matplotlib.pyplot as plt
plt.plot(LC, fcc_energies)
plt.xlabel('Lattice constant ($\AA$)')
plt.ylabel('Total energy (eV)')
plt.savefig('images/Cu-fcc.png')
print '#+tblname: cu-fcc-energies'
print r'| lattice constant ($\AA$) | Total Energy (eV) |'
for lc, e in zip(LC, fcc_energies):
    print '| {0} | {1} |'.format(lc, e)