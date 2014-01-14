from jasp import *
with jasp('molecules/O2-sp-singlet') as calc:
    print 'singlet: {0} eV'.format(calc.get_atoms().get_potential_energy())
with jasp('molecules/O2-sp-triplet') as calc:
    print 'triplet: {0} eV'.format(calc.get_atoms().get_potential_energy())