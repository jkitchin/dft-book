from jasp import *
# don't forget to normalize your total energy to a formula unit. Cu2O
# has 3 atoms, so the number of formula units in an atoms is
# len(atoms)/3.
with jasp('bulk/Cu2O-U=4.0') as calc:
    atoms = calc.get_atoms()
    cu2o_energy = atoms.get_potential_energy()/(len(atoms)/3)
with jasp('bulk/CuO-U=4.0') as calc:
    atoms = calc.get_atoms()
    cuo_energy = atoms.get_potential_energy()/(len(atoms)/2)
# make sure to use the same cutoff energy for the O2 molecule!
with jasp('molecules/O2-sp-triplet-400') as calc:
    atoms = calc.get_atoms()
    o2_energy = atoms.get_potential_energy()
rxn_energy = 4.0*cuo_energy - o2_energy - 2.0*cu2o_energy
print 'Reaction energy  = {0} eV'.format(rxn_energy)
print 'Corrected energy = {0} eV'.format(rxn_energy - 1.36)