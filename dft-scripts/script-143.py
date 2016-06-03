from vasp import Vasp
# don't forget to normalize your total energy to a formula unit. Cu2O
# has 3 atoms, so the number of formula units in an atoms is
# len(atoms)/3.
calc = Vasp('bulk/Cu2O')
atoms1 = calc.get_atoms()
cu2o_energy = atoms1.get_potential_energy()
calc = Vasp('bulk/CuO')
atoms2 = calc.get_atoms()
cuo_energy = atoms2.get_potential_energy()
# make sure to use the same cutoff energy for the O2 molecule!
calc = Vasp('molecules/O2-sp-triplet-400')
atoms3 = calc.get_atoms()
o2_energy = atoms3.get_potential_energy()
calc.stop_if(None in [cu2o_energy, cuo_energy, o2_energy])
cu2o_energy /= (len(atoms1) / 3)  # note integer math
cuo_energy /= (len(atoms2) / 2)
rxn_energy = 4.0 * cuo_energy - o2_energy - 2.0 * cu2o_energy
print 'Reaction energy = {0} eV'.format(rxn_energy)