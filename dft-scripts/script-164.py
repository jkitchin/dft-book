from ase.lattice.surface import fcc111
from vasp import Vasp
slab = fcc111('Al', size=(1, 1, 4), vacuum=10.0)
calc = Vasp('surfaces/Al-bandstructure',
            xc='PBE',
            encut=300,
            kpts=[6, 6, 6],
            lcharg=True,  # you need the charge density
            lwave=True,   # and wavecar for the restart
            atoms=slab)
n, bands, p = calc.get_bandstructure(kpts_path=[(r'$\Gamma$', [0, 0, 0]),
                                                ('$K1$', [0.5, 0.0, 0.0]),
                                                ('$K1$', [0.5, 0.0, 0.0]),
                                                ('$K2$', [0.5, 0.5, 0.0]),
                                                ('$K2$', [0.5, 0.5, 0.0]),
                                                (r'$\Gamma$', [0, 0, 0]),
                                                (r'$\Gamma$', [0, 0, 0]),
                                                ('$K3$', [0.0, 0.0, 1.0])],
                                     kpts_nintersections=10)
p.savefig('images/Al-slab-bandstructure.png')