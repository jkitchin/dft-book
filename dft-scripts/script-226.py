# Benzene on the slab
from vasp import Vasp
from ase.lattice.surface import fcc111, add_adsorbate
from ase.structure import molecule
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
print(Vasp('surfaces/Au-benzene-pbe-d2',
          xc='PBE',
          encut=350,
          kpts=[4, 4, 1],
          ibrion=1,
          nsw=100,
          lvdw=True,
          atoms=atoms).potential_energy)