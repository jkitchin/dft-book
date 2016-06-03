from vasp import Vasp
from ase import Atom, Atoms
bond_lengths = [1.05, 1.1, 1.15, 1.2, 1.25]
ATOMS = [Atoms([Atom('C', [0, 0, 0]),
                Atom('O', [d, 0, 0])],
               cell=(6, 6, 6))
         for d in bond_lengths]
calcs = [Vasp('molecules/co-{0}'.format(d),  # output dir
                xc='PBE',
                nbands=6,
                encut=350,
                ismear=1,
                sigma=0.01,
                atoms=atoms)
         for d, atoms in zip(bond_lengths, ATOMS)]
energies = [atoms.get_potential_energy() for atoms in ATOMS]
print(energies)