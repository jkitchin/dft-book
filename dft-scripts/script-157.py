from ase.lattice.surface import fcc111
atoms = fcc111('Al', size=(2, 2, 4), vacuum=10.0)
print([atom.z for atom in atoms])
print [atom.z <= 13 for atom in atoms]