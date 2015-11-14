from jasp import *
with jasp('surfaces/Ag-110') as calc:
    slab = calc.get_atoms()
    eslab = slab.get_potential_energy()
with jasp('surfaces/Ag-110-missing-row') as calc:
    missingrow = calc.get_atoms()
    emissingrow = missingrow.get_potential_energy()
with jasp('bulk/Ag-fcc') as calc:
    bulk = calc.get_atoms()
    ebulk = bulk.get_potential_energy()
print 'natoms slab        = {0}'.format(len(slab))
print 'natoms missing row = {0}'.format(len(missingrow))
print 'natoms bulk        = {0}'.format(len(bulk))
print 'dE = {0:1.3f} eV'.format(emissingrow + ebulk - eslab)