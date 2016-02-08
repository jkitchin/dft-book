from jasp import *
# bulk energy 1
with jasp('bulk/alloy/cu') as calc:
    atoms = calc.get_atoms()
    cu = atoms.get_potential_energy()/len(atoms)
# bulk energy 2
with jasp('bulk/alloy/pd') as calc:
    atoms = calc.get_atoms()
    pd = atoms.get_potential_energy()/len(atoms)
with jasp('bulk/alloy/cupd-1') as calc:
    atoms = calc.get_atoms()
    e1 = atoms.get_potential_energy()
    # subtract bulk energies off of each atom in cell
    for atom in atoms:
        if atom.symbol == 'Cu':
            e1 -= cu
        else:
            e1 -= pd
    e1 /= len(atoms)  # normalize by number of atoms in cell
with jasp('bulk/alloy/cupd-2') as calc:
    atoms = calc.get_atoms()
    e2 = atoms.get_potential_energy()
    for atom in atoms:
        if atom.symbol == 'Cu':
            e2 -= cu
        else:
            e2 -= pd
    e2 /= len(atoms)
print 'Delta Hf cupd-1 = {0:1.2f} eV/atom'.format(e1)
print 'Delta Hf cupd-2 = {0:1.2f} eV/atom'.format(e2)