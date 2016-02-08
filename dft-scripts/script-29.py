#!/usr/bin/env python
from ase import *
from ase.structure import molecule
from jasp import *
### Setup calculators
benzene = molecule('C6H6')
benzene.set_cell([10, 10, 10])
benzene.center()
with jasp('molecules/benzene',
          xc='PBE',
          nbands=18,
          encut=350,
          atoms=benzene) as calc:
    print(benzene.get_potential_energy())
    x1, y1, z1, cd1 = calc.get_charge_density()
chlorobenzene =  molecule('C6H6')
chlorobenzene.set_cell([10, 10, 10])
chlorobenzene.center()
chlorobenzene[11].symbol ='Cl'
with jasp('molecules/chlorobenzene',
          xc='PBE',
          nbands=18,
          encut=350,
          atoms=chlorobenzene) as calc:
    chlorobenzene.get_potential_energy()
    x2, y2, z2, cd2 = calc.get_charge_density()
cdiff = cd2 - cd1
print(cdiff.min(), cdiff.max())
##########################################
##### set up visualization of charge difference
from enthought.mayavi import mlab
mlab.contour3d(x1, y1, z1, cdiff,
               contours=[-0.02, 0.02])
mlab.savefig('images/cdiff.png')
mlab.show()