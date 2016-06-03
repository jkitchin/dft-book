from vasp import Vasp
from ase.lattice.surface import fcc111
atoms = fcc111('Al', size=(1, 1, 4), vacuum=10.0)
calc = Vasp('surfaces/Al-slab-unrelaxed',
            xc='PBE',
            kpts=[6, 6, 1],
            encut=350,
            atoms=atoms)
print(atoms.get_forces())