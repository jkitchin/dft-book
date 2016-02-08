from jasp import *
from ase import Atom, Atoms
# parent metals
with jasp('bulk/alloy/cu') as calc:
    atoms = calc.get_atoms()
    cu = atoms.get_potential_energy()/len(atoms)
with jasp('bulk/alloy/pd') as calc:
    atoms = calc.get_atoms()
    pd = atoms.get_potential_energy()/len(atoms)
atoms = Atoms([Atom('Cu',  [-1.867,     1.867,      0.000]),
               Atom('Cu',  [0.000,      0.000,      0.000]),
               Atom('Cu',  [0.000,      1.867,      1.867]),
               Atom('Pd',  [-1.867,     0.000,      1.86])],
               cell=[[-3.735,  0.000,  0.000],
                     [0.000,  0.000,  3.735],
                     [0.000,  3.735,  0.000]])
with jasp('bulk/alloy/cu3pd-2',
          xc='PBE',
          encut=350,
          kpts=(8, 8, 8),
          nbands=34,
          ibrion=2,
          isif=3,
          nsw=10,
          atoms=atoms) as calc:
    e4 = atoms.get_potential_energy()
    for atom in atoms:
        if atom.symbol == 'Cu':
            e4 -= cu
        else:
            e4 -= pd
    e4 /= len(atoms)
print 'Delta Hf cu3pd-2 = {0:1.2f} eV/atom'.format(e4)