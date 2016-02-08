from jasp import *
from ase import Atom, Atoms
# parent metals
with jasp('bulk/alloy/cu') as calc:
    atoms = calc.get_atoms()
    cu = atoms.get_potential_energy()/len(atoms)
with jasp('bulk/alloy/pd') as calc:
    atoms = calc.get_atoms()
    pd = atoms.get_potential_energy()/len(atoms)
atoms = Atoms([Atom('Cu',  [-3.672,     3.672,      3.672]),
               Atom('Cu',  [0.000,     0.000,      0.000]),
               Atom('Cu',  [-10.821,   10.821,     10.821]),
               Atom('Pd',  [-7.246,     7.246,      7.246])],
               cell=[[-5.464,  3.565,  5.464],
                     [-3.565,  5.464,  5.464],
                     [-5.464,  5.464,  3.565]])
with jasp('bulk/alloy/cu3pd-1',
          xc='PBE',
          encut=350,
          kpts=(8, 8, 8),
          nbands=34,
          ibrion=2,
          isif=3,
          nsw=10,
          atoms=atoms) as calc:
    e3 = atoms.get_potential_energy()
    for atom in atoms:
        if atom.symbol == 'Cu':
            e3 -= cu
        else:
            e3 -= pd
    e3 /= len(atoms)
print 'Delta Hf cu3pd-1 = {0:1.2f} eV/atom'.format(e3)