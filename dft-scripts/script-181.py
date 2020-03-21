from vasp import Vasp
eslab = Vasp('surfaces/Ag-110').potential_energy
emissingrow = Vasp('surfaces/Ag-110-missing-row').potential_energy
ebulk = Vasp('bulk/Ag-fcc').potential_energy
print 'dE = {0:1.3f} eV'.format(emissingrow + ebulk - eslab)