from ase.lattice.hexagonal import HexagonalClosedPacked
from jasp import *
import matplotlib.pyplot as plt
atoms = HexagonalClosedPacked(symbol='Ru',
                              latticeconstant={'a': 2.7,
                                               'c/a': 1.584})
a_list = [2.5, 2.6, 2.7, 2.8, 2.9]
covera_list = [1.4, 1.5, 1.6, 1.7, 1.8]
for a in a_list:
    energies = []
    for covera in covera_list:
        atoms = HexagonalClosedPacked(symbol='Ru',
                              latticeconstant={'a': a,
                                               'c/a': covera})
        wd = 'bulk/Ru/{0:1.2f}-{1:1.2f}'.format(a, covera)
        with jasp(wd,
                  xc='PBE',
                  # the c-axis is longer than the a-axis, so we use
                  # fewer kpoints.
                  kpts=(6, 6, 4), 
                  encut=350,
                  atoms=atoms) as calc:
            try:
                energies.append(atoms.get_potential_energy())
            except (VaspSubmitted, VaspQueued):
                pass
    plt.plot(covera_list, energies, label=r'a={0} $\AA$'.format(a))
plt.xlabel('$c/a$')
plt.ylabel('Energy (eV)')
plt.legend()
plt.savefig('images/Ru-covera-scan.png')
plt.show()