from vasp import Vasp
calc = Vasp('molecules/h2o-bader')
calc.bader(ref=True, overwrite=True)
atoms = calc.get_atoms()
for atom in atoms:
    print('|{0} | {1} |'.format(atom.symbol, atom.charge))