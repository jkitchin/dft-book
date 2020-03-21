from vasp import Vasp
from ase import Atom, Atoms
# parent metals
cu = Vasp('bulk/alloy/cu')
cu_e = cu.potential_energy / len(cu.get_atoms())
pd = Vasp('bulk/alloy/pd')
pd_e = pd.potential_energy / len(pd.get_atoms())
atoms = Atoms([Atom('Cu',  [-1.867,     1.867,      0.000]),
               Atom('Cu',  [0.000,      0.000,      0.000]),
               Atom('Cu',  [0.000,      1.867,      1.867]),
               Atom('Pd',  [-1.867,     0.000,      1.86])],
               cell=[[-3.735,  0.000,  0.000],
                     [0.000,  0.000,  3.735],
                     [0.000,  3.735,  0.000]])
calc = Vasp('bulk/alloy/cu3pd-2',
            xc='PBE',
            encut=350,
            kpts=[8, 8, 8],
            nbands=34,
            ibrion=2,
            isif=3,
            nsw=10,
            atoms=atoms)
e4 = atoms.get_potential_energy()
Vasp.wait(abort=True)
for atom in atoms:
    if atom.symbol == 'Cu':
        e4 -= cu_e
    else:
        e4 -= pd_e
e4 /= len(atoms)
print('Delta Hf cu3pd-2 = {0:1.2f} eV/atom'.format(e4))