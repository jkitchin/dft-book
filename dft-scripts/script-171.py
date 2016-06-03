from ase.lattice.surface import fcc110
from ase.io import write
from ase.constraints import FixAtoms
from ase.visualize import view
atoms = fcc110('Au', size=(2, 1, 6), vacuum=10.0)
constraint = FixAtoms(mask=[atom.tag > 2 for atom in atoms])
atoms.set_constraint(constraint)
view(atoms)