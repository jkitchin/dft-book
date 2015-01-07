from jasp import *
from ase import Atom, Atoms
bond_lengths = [1.05, 1.1, 1.15, 1.2, 1.25]
energies = []
for d in bond_lengths:  # possible bond lengths
    co = Atoms([Atom('C', [0, 0, 0]),
                Atom('O', [d, 0, 0])],
               cell=(6, 6, 6))
    with jasp('molecules/co-{0}'.format(d),  # output dir
              xc='PBE',
              nbands=6,
              encut=350,
              ismear=1,
              sigma=0.01,
              atoms=co):
        try:
            e = co.get_potential_energy()
            energies.append(e)
            print 'd = {0:1.2f} ang'.format(d)
            print 'energy = {0:1.3f} eV'.format(e)
            print 'forces = (eV/ang)\n {0}'.format(co.get_forces())
            print ''  # blank line
        except (VaspSubmitted, VaspQueued):
            energies.append(None)
            pass
if None not in energies:
    import matplotlib.pyplot as plt
    plt.plot(bond_lengths, energies, 'bo-')
    plt.xlabel(r'Bond length ($\AA$)')
    plt.ylabel('Total energy (eV)')
    plt.savefig('images/co-bondlengths.png')