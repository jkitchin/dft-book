from jasp import *
with jasp('bulk/alloy/cupd-1') as calc:
    atoms = calc.get_atoms()
    e1 = atoms.get_potential_energy()/len(atoms)
with jasp('bulk/alloy/cupd-2') as calc:
    atoms = calc.get_atoms()
    e2 = atoms.get_potential_energy()/len(atoms)
print 'cupd-1: {0} eV/atom'.format(e1)
print 'cupd-2: {0} eV/atom'.format(e2)