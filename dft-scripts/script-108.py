from jasp import *
with jasp('bulk/atomic-rh') as calc:
    atoms = calc.get_atoms()
    atomic_energy = atoms.get_potential_energy()
with jasp('bulk/bulk-rh') as calc:
    atoms = calc.get_atoms()
kpts = [3, 4, 6, 9, 12, 15, 18]
for k in kpts:
    with jasp('bulk/bulk-rh-kpts-{0}'.format(k),
          xc='PBE',
          encut=350,
          kpts=(k, k, k),
          atoms=atoms) as calc:
        e = atoms.get_potential_energy()
    print '({0:2d}, {0:2d}, {0:2d}): cohesive energy = {1} eV'.format(k,e-atomic_energy)