from ase.lattice.surface import fcc111
from ase.io import write
from jasp import *
from jasp.jasp_bandstructure import *
slab = fcc111('Al', size=(1,1,4), vacuum=10.0)
with jasp('surface/Al-bandstructure',
          xc='PBE',
          encut=300,
          kpts=(6,6,6),
          atoms=slab) as calc:
    n,bands,p  = calc.get_bandstructure(kpts_path=[('$\Gamma$', [0,0,0]),
                                                   ('$K1$', [0.5, 0.0, 0.0]),
                                                   ('$K1$', [0.5,0.0,0.0]),
                                                   ('$K2$', [0.5,0.5,0.0]),
                                                   ('$K2$', [0.5,0.5,0.0]),
                                                   ('$\Gamma$', [0,0,0]),
                                                   ('$\Gamma$', [0,0,0]),
                                                   ('$K3$', [0.0, 0.0, 1.0])],
                                                   kpts_nintersections=10)
p.savefig('images/Al-slab-bandstructure.png')
p.show()