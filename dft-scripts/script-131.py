# run the anatase calculations
import numpy as np
from vasp import Vasp
from ase import Atom, Atoms
# http://cst-www.nrl.navy.mil/lattice/struk/c5.html
B = 'Ti'; X = 'O'; a = 3.7842; c = 2*4.7573; z = 0.0831;
a1 = a * np.array([1.0, 0.0, 0.0])
a2 = a * np.array([0.0, 1.0, 0.0])
a3 = np.array([0.5 * a, 0.5 * a, 0.5 * c])
atoms = Atoms([Atom(B, -0.125 * a1 + 0.625 * a2 + 0.25 * a3),
               Atom(B,  0.125 * a1 + 0.375 * a2 + 0.75 * a3),
               Atom(X, -z*a1 + (0.25-z)*a2 + 2.*z*a3),
               Atom(X, -(0.25+z)*a1 + (0.5-z)*a2 + (0.5+2*z)*a3),
               Atom(X, z*a1 - (0.25 - z)*a2 + (1-2*z)*a3),
               Atom(X, (0.25 + z)*a1 + (0.5 + z)*a2 + (0.5-2*z)*a3)],
               cell=[a1,a2,a3])
nTiO2 = len(atoms) / 3.
v0 = atoms.get_volume()
cell0 = atoms.get_cell()
volumes = [30., 33., 35., 37., 39.]  #vol of one TiO2
for v in volumes:
    atoms.set_cell(cell0 * ((nTiO2*v/v0)**(1./3.)),
                   scale_atoms=True)
    calc = Vasp('bulk/TiO2/anatase/anatase-{0}'.format(v),
                encut=350,
                kpts=[6, 6, 6],
                xc='PBE',
                ismear=0,
                sigma=0.001,
                isif=2,
                ibrion=2,
                nsw=20,
                atoms=atoms)
    calc.update()