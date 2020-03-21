from vasp import Vasp
calc = Vasp('surfaces/Al-slab-unrelaxed')
atoms = calc.get_atoms()
print 'Total energy: {0:1.3f} eV'.format(atoms.get_potential_energy())
for i in range(1, len(atoms)):
    print '{0}  deltaz = {1:1.3f} angstroms'.format(i, atoms[i].z - atoms[i-1].z)