# Benzene on the slab
from jasp import *
from ase.lattice.surface import fcc111, add_adsorbate
from ase.data.molecules import molecule
from ase.constraints import FixAtoms
atoms = fcc111('Au', size=(3,3,3), vacuum=10)
benzene = molecule('C6H6')
benzene.translate(-benzene.get_center_of_mass())
# I want the benzene centered on the position in the middle of atoms
# 20, 22, 23 and 25
p = (atoms.positions[20] +
     atoms.positions[22] +
     atoms.positions[23] +
     atoms.positions[25])/4.0 + [0.0, 0.0, 3.05]
benzene.translate(p)
atoms += benzene
# now we constrain the slab
c = FixAtoms(mask=[atom.symbol=='Au' for atom in atoms])
atoms.set_constraint(c)
#from ase.visualize import view; view(atoms)
with jasp('surfaces/Au-benzene-pbe',
          xc='PBE',
          encut=350,
          kpts=(4,4,1),
          ibrion=1,
          nsw=100,
          atoms=atoms) as calc:
    print atoms.get_potential_energy()