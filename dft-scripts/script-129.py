from ase import Atoms
atoms = Atoms('Cu2O')
MW = atoms.get_masses().sum()
H = 1. # kJ/g
print 'rxn energy = {0:1.1f} eV'.format(-2*H*MW/96.4)  # convert to eV