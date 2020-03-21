from vasp import Vasp
from ase.lattice.surface import fcc111
calc = Vasp('surfaces/Al-slab-relaxed')
atoms = calc.get_atoms()
print 'Total energy: {0:1.3f}'.format(atoms.get_potential_energy())
for i in range(1, len(atoms)):
    print 'd_({0},{1}) = {2:1.3f} angstroms'.format(i, i-1,
                                                    atoms[i].z - atoms[i-1].z)