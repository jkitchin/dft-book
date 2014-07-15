import textwrap
from ase.data.molecules import molecule
atoms = molecule('CH3CH2OH')
print atoms
#delete all the hydrogens
ind2del = [atom.index for atom in atoms if atom.symbol=='H']
print 'Indices to delete: ',ind2del
del atoms[ind2del]
# now print what is left
print atoms