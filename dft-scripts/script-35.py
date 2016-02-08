from jasp import *
from ase import Atom, Atoms
from ase.io import write
from enthought.mayavi import mlab
from ase.data import vdw_radii
from ase.data.colors import cpk_colors
atoms = Atoms([Atom('C',  [ 0.0000,	0.0000,		-0.8088]),
               Atom('Br', [ 0.0000,	0.0000,		 1.1146]),
               Atom('F',  [ 0.0000,	1.2455,		-1.2651]),
               Atom('F',  [ 1.0787,    -0.6228,		-1.2651]),
               Atom('F',  [-1.0787,    -0.6228,		-1.2651])],
               cell=(10, 10, 10))
atoms.center()
with jasp('molecules/CF3Br',
          encut=350,
          xc='PBE',
          ibrion=1,
          nsw=50,
          lvtot=True,
          lvhar=True,
          atoms=atoms) as calc:
    calc.set_nbands(f=2)
    calc.calculate()
    x, y, z, lp = calc.get_local_potential()
    x, y, z, cd = calc.get_charge_density()
mlab.figure(1, bgcolor=(1, 1, 1)) # make a white figure
# plot the atoms as spheres
for atom in atoms:
    mlab.points3d(atom.x,
                  atom.y,
                  atom.z,
                  scale_factor=vdw_radii[atom.number]/5.,
                  resolution=20,
                  # a tuple is required for the color
                  color=tuple(cpk_colors[atom.number]),
                  scale_mode='none')
# plot the bonds. We want a line from C-Br, C-F, etc...
# We create a bond matrix showing which atoms are connected.
bond_matrix = [[0, 1],
               [0, 2],
               [0, 3],
               [0, 4]]
for a1, a2 in bond_matrix:
    mlab.plot3d(atoms.positions[[a1,a2], 0], # x-positions
                atoms.positions[[a1,a2], 1], # y-positions
                atoms.positions[[a1,a2], 2], # z-positions
                [2, 2],
                tube_radius=0.02,
                colormap='Reds')
mlab.contour3d(x, y, z, lp)
mlab.savefig('images/halogen-ep.png')
mlab.show()