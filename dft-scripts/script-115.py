# run the rutile calculations
from jasp import *
from ase import Atom, Atoms
B='Ti'; X='O'; a=4.59; c=2.958; u=0.305;
'''
create a rutile structure from the lattice vectors at
http://cst-www.nrl.navy.mil/lattice/struk/c4.html
spacegroup: 136 P4_2/mnm
'''
a1 = a*np.array([1.0, 0.0, 0.0])
a2 = a*np.array([0.0, 1.0, 0.0])
a3 = c*np.array([0.0, 0.0, 1.0])
atoms = Atoms([Atom(B, [0., 0., 0.]),
               Atom(B, 0.5*a1 + 0.5*a2 + 0.5*a3),
               Atom(X,  u*a1 + u*a2),
               Atom(X, -u*a1 - u*a2),
               Atom(X, (0.5+u)*a1 + (0.5-u)*a2 + 0.5*a3),
               Atom(X, (0.5-u)*a1 + (0.5+u)*a2 + 0.5*a3)],
               cell=[a1, a2, a3])
nTiO2 = len(atoms)/3.
v0 = atoms.get_volume()
cell0 = atoms.get_cell()
volumes = [28., 30., 32., 34., 36.]  #vol of one TiO2
for v in volumes:
    atoms.set_cell(cell0*((nTiO2*v/v0)**(1./3.)), scale_atoms=True)
    with jasp('bulk/TiO2/rutile/rutile-{0}'.format(v),
              encut=350,
              kpts=(6,6,6),
              xc='PBE',
              ismear=0,
              sigma=0.001,
              isif=2,
              ibrion=2,
              nsw=20,
              atoms=atoms) as calc:
        try:
            calc.calculate()
        except (VaspSubmitted, VaspQueued):
            pass