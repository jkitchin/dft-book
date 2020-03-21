from vasp import Vasp
from ase import Atom, Atoms
from ase.utils.eos import EquationOfState
import numpy as np
LC = [3.75, 3.80, 3.85, 3.90, 3.95, 4.0, 4.05, 4.1]
GGA = {'AM': 'AM05',
       'PE': 'PBE',
       'PS': 'PBEsol',
       'RP': 'RPBE'}
for key in GGA:
    volumes, energies = [], []
    for a in LC:
        atoms = Atoms([Atom('Pd', (0, 0, 0))],
                      cell=0.5 * a * np.array([[1.0, 1.0, 0.0],
                                               [0.0, 1.0, 1.0],
                                               [1.0, 0.0, 1.0]]))
        calc = Vasp('bulk/Pd-GGA-{1}-{0}'.format(a, key),
                    encut=350,
                    kpts=[12, 12, 12],
                    xc='LDA',
                    gga=key,
                    atoms=atoms)
        e = atoms.get_potential_energy()
        energies.append(e)
        volumes.append(atoms.get_volume())
    if None not in energies:
        eos = EquationOfState(volumes, energies)
        v0, e0, B = eos.fit()
        print '{1:6s} lattice constant is {0:1.3f} Ang^3'.format((4*v0)**(1./3.),
                                                             GGA[key])
    else:
        print energies, LC
        print '{0} is not ready'.format(GGA[key])