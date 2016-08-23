from vasp import Vasp
from ase import Atom, Atoms
# parent metals
atoms = Vasp('bulk/alloy/cu').get_atoms()
cu = atoms.get_potential_energy() / len(atoms)
atoms = Vasp('bulk/alloy/pd').get_atoms()
pd = atoms.get_potential_energy() / len(atoms)
atoms = Atoms([Atom('Cu',  [-3.672,     3.672,      3.672]),
               Atom('Cu',  [0.000,     0.000,      0.000]),
               Atom('Cu',  [-10.821,   10.821,     10.821]),
               Atom('Pd',  [-7.246,     7.246,      7.246])],
               cell=[[-5.464,  3.565,  5.464],
                     [-3.565,  5.464,  5.464],
                     [-5.464,  5.464,  3.565]])
calc = Vasp('bulk/alloy/cu3pd-1',
            xc='PBE',
            encut=350,
            kpts=[8, 8, 8],
            nbands=34,
            ibrion=2,
            isif=3,
            nsw=10,
            atoms=atoms)
e3 = atoms.get_potential_energy()
Vasp.wait(abort=True)
for atom in atoms:
    if atom.symbol == 'Cu':
        e3 -= cu
    else:
        e3 -= pd
e3 /= len(atoms)
print 'Delta Hf cu3pd-1 = {0:1.2f} eV/atom'.format(e3)