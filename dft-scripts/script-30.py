#!/usr/bin/env python
from ase import *
from ase.structure import molecule
from vasp import Vasp
### Setup calculators
benzene = molecule('C6H6')
benzene.set_cell([10, 10, 10])
benzene.center()
calc1 = Vasp('molecules/benzene',
            xc='PBE',
            nbands=18,
            encut=350,
            atoms=benzene)
calc1.set(lcharg=True)
chlorobenzene =  molecule('C6H6')
chlorobenzene.set_cell([10, 10, 10])
chlorobenzene.center()
chlorobenzene[11].symbol ='Cl'
calc2 = Vasp('molecules/chlorobenzene',
            xc='PBE',
            nbands=22,
            encut=350,
            atoms=chlorobenzene)
calc2.set(lcharg=True)
calc2.stop_if(None in (calc1.potential_energy, calc2.potential_energy))
x1, y1, z1, cd1 = calc1.get_charge_density()
x2, y2, z2, cd2 = calc2.get_charge_density()
cdiff = cd2 - cd1
print(cdiff.min(), cdiff.max())
##########################################
##### set up visualization of charge difference
from enthought.mayavi import mlab
mlab.contour3d(x1, y1, z1, cdiff,
               contours=[-0.02, 0.02])
mlab.savefig('images/cdiff.png')