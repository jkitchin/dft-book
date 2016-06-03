# step 1 frozen atoms and shape at different volumes
from ase import Atom, Atoms
import numpy as np
from vasp import Vasp
import matplotlib.pyplot as plt
'''
create a TiO2 structure from the lattice vectors at
http://cst-www.nrl.navy.mil/lattice/struk/c4.html
'''
a = 4.59  # experimental degrees of freedom.
c = 2.96
u = 0.3  # internal degree of freedom!
#primitive vectors
a1 = a * np.array([1.0, 0.0, 0.0])
a2 = a * np.array([0.0, 1.0, 0.0])
a3 = c * np.array([0.0, 0.0, 1.0])
atoms = Atoms([Atom('Ti', [0., 0., 0.]),
               Atom('Ti', 0.5 * a1 + 0.5 * a2 + 0.5 * a3),
               Atom('O', u * a1 + u * a2),
               Atom('O', -u * a1 - u * a2),
               Atom('O', (0.5 + u) * a1 + (0.5 - u) * a2 + 0.5 * a3),
               Atom('O', (0.5 - u) * a1 + (0.5 + u) * a2 + 0.5 * a3)],
              cell=[a1, a2, a3])
v0 = atoms.get_volume()
cell0 = atoms.get_cell()
factors = [0.9, 0.95, 1.0, 1.05, 1.1] #to change volume by
energies, volumes = [], []
ready = True
for f in factors:
    v1 = f * v0
    cell_factor = (v1 / v0)**(1. / 3.)
    atoms.set_cell(cell0 * cell_factor, scale_atoms=True)
    calc = Vasp('bulk/tio2/step1-{0:1.2f}'.format(f),
                encut=520,
                kpts=[5, 5, 5],
                isif=2, # relax internal degrees of freedom
                ibrion=1,
                nsw=50,
                xc='PBE',
                sigma=0.05,
                atoms=atoms)
    energies.append(atoms.get_potential_energy())
    volumes.append(atoms.get_volume())
calc.stop_if(None in energies)
plt.plot(volumes, energies)
plt.xlabel('Vol. ($\AA^3)$')
plt.ylabel('Total energy (eV)')
plt.savefig('images/tio2-step1.png')
print '#+tblname: tio2-vol-ene'
print '#+caption: Total energy of TiO_{2} vs. volume.'
print '| Volume ($\AA^3$) | Energy (eV) |'
print '|-'
for v, e in zip(volumes, energies):
    print '| {0} | {1} |'.format(v, e)