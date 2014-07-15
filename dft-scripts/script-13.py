from ase.data.molecules import molecule
atoms = molecule('C6H6')
masses = atoms.get_masses()
molecular_weight = masses.sum()
molecular_formula = atoms.get_chemical_symbols(reduce=True)
# note use of two lines to keep length of line reasonable
s = 'The molecular weight of {0} is {1:1.2f} gm/mol'
print s.format(molecular_formula, molecular_weight)