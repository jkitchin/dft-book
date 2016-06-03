from vasp import Vasp
from ase import Atom, Atoms
atoms = Atoms([Atom('Cu',  [0.000,      0.000,      0.000]),
               Atom('Pd',  [-1.652,     0.000,      2.039])],
              cell=  [[0.000, -2.039,  2.039],
                      [0.000,  2.039,  2.039],
                      [-3.303,  0.000,  0.000]])
atoms = atoms.repeat((2, 2, 2))
calc = Vasp('bulk/CuPd-cls-0',
            xc='PBE',
            encut=350,
            kpts=[4, 4, 4],
            ibrion=2,
            isif=3,
            nsw=40,
            atoms=atoms)
print(atoms.get_potential_energy())