from vasp import Vasp
from ase import Atom, Atoms
from ase.utils.eos import EquationOfState
import numpy as np
LC = [3.75, 3.80, 3.85, 3.90, 3.95, 4.0, 4.05, 4.1]
volumes, energies = [], []
for a in LC:
    atoms = Atoms([Atom('Pd', (0, 0, 0))],
                  cell=0.5 * a * np.array([[1.0, 1.0, 0.0],
                                           [0.0, 1.0, 1.0],
                                           [1.0, 0.0, 1.0]]))
    calc = Vasp('bulk/Pd-LDA-{0}'.format(a),
                encut=350,
                kpts=[12, 12, 12],
                xc='LDA',
                atoms=atoms)
    e = atoms.get_potential_energy()
    energies.append(e)
    volumes.append(atoms.get_volume())
calc.stop_if(None in energies)
eos = EquationOfState(volumes, energies)
v0, e0, B = eos.fit()
print('LDA lattice constant is {0:1.3f} Ang^3'.format((4*v0)**(1./3.)))