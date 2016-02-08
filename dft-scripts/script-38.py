from jasp import *
from ase.io.bader import attach_charges
from ase.units import Bohr
with jasp('molecules/h2o-bader') as calc:
    atoms = calc.get_atoms()
    symbols = np.array(atoms.get_chemical_symbols())[calc.sort]
    pos = atoms.positions[calc.sort] * Bohr
    newatoms = Atoms(symbols, positions=pos, cell=atoms.get_cell())
    attach_charges(newatoms, 'ACF.dat')
    print('#+tblname: bader')
    print('#+caption: Bader charges for a water molecule')
    print('| atom | Bader charge|')
    print('|-')
    for atom in newatoms:
        print('|{0} | {1} |'.format(atom.symbol, atom.charge))