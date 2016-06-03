from vasp import Vasp
calc = Vasp('bulk/atomic-rh')
atomic_energy = calc.potential_energy
calc = Vasp('bulk/bulk-rh')
atoms = calc.get_atoms()
kpts = [3, 4, 6, 9, 12, 15, 18]
calcs = [Vasp('bulk/bulk-rh-kpts-{0}'.format(k),
                xc='PBE',
                encut=350,
                kpts=[k, k, k],
                atoms=atoms)
         for k in kpts]
energies = [calc.potential_energy for calc in calcs]
calcs[0].stop_if(None in energies)
for k, e in zip(kpts, energies):
    print('({0:2d}, {0:2d}, {0:2d}):'
          ' cohesive energy = {1} eV'.format(k,
                                             e - atomic_energy))