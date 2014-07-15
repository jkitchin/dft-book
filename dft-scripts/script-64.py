from jasp import *
from ase import Atom, Atoms
with jasp('molecules/O2-sp-singlet') as calc:
    calc.clone('molecules/O2-sp-singlet-magmoms')
with jasp('molecules/O2-sp-singlet-magmoms') as calc:
    calc.set(lorbit=11)
    atoms = calc.get_atoms()
    magmoms = atoms.get_magnetic_moments()
    print 'singlet ground state'
    for i,atom in enumerate(atoms):
        print 'atom {0}: magmom = {1}'.format(i, magmoms[i])
    print atoms.get_magnetic_moment()
with jasp('molecules/O2-sp-triplet') as calc:
    calc.clone('molecules/O2-sp-triplet-magmoms')
with jasp('molecules/O2-sp-triplet-magmoms') as calc:
    calc.set(lorbit=11)
    atoms = calc.get_atoms()
    magmoms = atoms.get_magnetic_moments()
    print
    print 'triplet ground state'
    for i,atom in enumerate(atoms):
        print 'atom {0}: magmom = {1}'.format(i, magmoms[i])
    print atoms.get_magnetic_moment()