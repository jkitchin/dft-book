from vasp import Vasp
# bulk energy 1
calc = Vasp('bulk/alloy/cu')
atoms = calc.get_atoms()
cu = atoms.get_potential_energy()/len(atoms)
# bulk energy 2
calc = Vasp('bulk/alloy/pd')
atoms = calc.get_atoms()
pd = atoms.get_potential_energy()/len(atoms)
calc = Vasp('bulk/alloy/cupd-1')
atoms = calc.get_atoms()
e1 = atoms.get_potential_energy()
# subtract bulk energies off of each atom in cell
for atom in atoms:
    if atom.symbol == 'Cu':
        e1 -= cu
    else:
        e1 -= pd
e1 /= len(atoms)  # normalize by number of atoms in cell
calc = Vasp('bulk/alloy/cupd-2')
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