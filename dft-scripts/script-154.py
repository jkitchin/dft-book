from vasp import Vasp
from ase import Atom, Atoms
from ase.visualize import view
a = 5.38936
atoms = Atoms([Atom('Si', [0, 0, 0]),
               Atom('Si', [0.25, 0.25, 0.25])])
atoms.set_cell([[a / 2., a / 2., 0.0],
                [0.0,  a / 2., a / 2.],
                [a / 2., 0.0, a / 2.]], scale_atoms=True)
calc = Vasp('bulk/Si-selfconsistent',
            xc='PBE',
            prec='Medium',
            lcharg=True,
            lwave=True,
            kpts=[4, 4, 4],
            atoms=atoms)
calc.run()