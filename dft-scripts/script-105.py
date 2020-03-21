from vasp import Vasp
from ase import Atom, Atoms
import numpy as np
LC = [2.75, 2.8, 2.85, 2.9, 2.95, 3.0]
for a in LC:
    atoms = Atoms([Atom('Cu', [0, 0, 0])],
                  cell=0.5 * a * np.array([[ 1.0,  1.0, -1.0],
                                           [-1.0,  1.0,  1.0],
                                           [ 1.0, -1.0,  1.0]]))
    calc = Vasp('bulk/Cu-bcc-{0}'.format(a),
                xc='PBE',
                encut=350,
                kpts=[8, 8, 8],
                atoms=atoms)
    print(calc.potential_energy)