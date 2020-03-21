from vasp import Vasp
print 'dE = {0:1.3f} eV'.format(Vasp('surfaces/Au-110-missing-row').potential_energy
                                + Vasp('bulk/Au-fcc').potential_energy
                                - Vasp('surfaces/Au-110').potential_energy)