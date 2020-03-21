from vasp import Vasp
eslab = Vasp('surfaces/Cu-110').potential_energy
emissingrow = Vasp('surfaces/Cu-110-missing-row').potential_energy
ebulk = Vasp('bulk/Cu-fcc').potential_energy
print 'natoms slab        = {0}'.format(len(slab))
print 'natoms missing row = {0}'.format(len(missingrow))
print 'natoms bulk        = {0}'.format(len(bulk))
print 'dE = {0:1.3f} eV'.format(emissingrow + ebulk - eslab)