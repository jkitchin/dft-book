from jasp import *
# bcc energies and volumes
bcc_LC = [2.75, 2.8, 2.85, 2.9, 2.95, 3.0]
bcc_volumes = []
bcc_energies = []
for a in bcc_LC:
    with jasp('bulk/Cu-bcc-{0}'.format(a)) as calc:
        atoms = calc.get_atoms()
        bcc_volumes.append(atoms.get_volume())
        bcc_energies.append(atoms.get_potential_energy())
# fcc energies and volumes
fcc_LC = [3.5, 3.55, 3.6, 3.65, 3.7, 3.75]
fcc_volumes = []
fcc_energies =[]
for a in fcc_LC:
    with jasp('bulk/Cu-{0}'.format(a)) as calc:
        atoms = calc.get_atoms()
        fcc_volumes.append(atoms.get_volume())
        fcc_energies.append(atoms.get_potential_energy())
import matplotlib.pyplot as plt
plt.plot(fcc_volumes, fcc_energies, label='fcc')
plt.plot(bcc_volumes, bcc_energies, label='bcc')
plt.xlabel('Atomic volume ($\AA^3$/atom)')
plt.ylabel('Total energy (eV)')
plt.legend()
plt.savefig('images/Cu-bcc-fcc.png')
# print table of data
print '#+tblname: bcc-data'
print '#+caption: Total energy vs. lattice constant for BCC Cu.'
print '| Lattice constant (\AA$^3$) | Total energy (eV) |'
print '|-'
for lc, e in zip(bcc_LC, bcc_energies):
    print '| {0} | {1} |'.format(lc, e)