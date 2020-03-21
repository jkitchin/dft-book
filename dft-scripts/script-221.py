# the clean gold slab
from vasp import Vasp
from ase.lattice.surface import fcc111, add_adsorbate
from ase.constraints import FixAtoms
atoms = fcc111('Au', size=(3,3,3), vacuum=10)
# now we constrain the slab
c = FixAtoms(mask=[atom.symbol=='Au' for atom in atoms])
atoms.set_constraint(c)
#from ase.visualize import view; view(atoms)
print(Vasp('surfaces/Au-pbe',
           xc='PBE',
           encut=350,
           kpts=[4, 4, 1],
           ibrion=1,
           nsw=100,
           atoms=atoms).potential_energy)