from vasp import Vasp
calc = Vasp('bulk/Cu2O-U=4.0')
atoms = calc.get_atoms()
cu2o_energy = atoms.get_potential_energy() / (len(atoms) / 3)
calc = Vasp('bulk/CuO-U=4.0')
atoms = calc.get_atoms()
cuo_energy = atoms.get_potential_energy() / (len(atoms) / 2)
# make sure to use the same cutoff energy for the O2 molecule!
calc = Vasp('molecules/O2-sp-triplet-400')
o2_energy = calc.results['energy']
calc.stop_if(None in [cu2o_energy, cuo_energy, o2_energy])
# don't forget to normalize your total energy to a formula unit. Cu2O
# has 3 atoms, so the number of formula units in an atoms is
# len(atoms)/3.
rxn_energy = 4.0 * cuo_energy - o2_energy - 2.0 * cu2o_energy
print('Reaction energy  = {0} eV'.format(rxn_energy))
print('Corrected energy = {0} eV'.format(rxn_energy - 1.36))