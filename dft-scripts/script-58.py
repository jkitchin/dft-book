from jasp import *
from ase import Atom, Atoms
sigmas = [0.2, 0.1, 0.05, 0.02, 0.01, 0.001]
D = []
for sigma in sigmas:
    atoms = Atoms([Atom('O',[5, 5, 5], magmom=2)],
                  cell=(10, 10, 10))
    with jasp('molecules/O-sp-triplet-sigma-{0}'.format(sigma),
              xc='PBE',
              encut=400,
              ismear=0,
              sigma=sigma,
              ispin=2,
              atoms=atoms) as calc:
        try:
            E_O = atoms.get_potential_energy()
        except (VaspSubmitted, VaspQueued):
            E_O = None
    # now relaxed O2 dimer
    atoms = Atoms([Atom('O',[5,    5, 5],magmom=1),
                   Atom('O',[6.22, 5, 5],magmom=1)],
                  cell=(10, 10, 10))
    with jasp('molecules/O2-sp-triplet-sigma-{0}'.format(sigma),
              xc='PBE',
              encut=400,
              ismear=0,
              sigma=sigma,
              ispin=2,   # turn spin-polarization on
              ibrion=2,  # make sure we relax the geometry
              nsw=10,
              atoms=atoms) as calc:
        try:
            E_O2 = atoms.get_potential_energy()
        except (VaspSubmitted, VaspQueued):
            E_O2 = None
    if None not in (E_O, E_O2):
        d = 2 * E_O - E_O2
        D.append(d)
        print 'O2 -> 2O sigma = {0}  D = {1:1.3f} eV'.format(sigma, d)
import matplotlib.pyplot as plt
plt.plot(sigmas, D, 'bo-')
plt.xlabel('SIGMA (eV)')
plt.ylabel('O$_2$ dissociation energy (eV)')
plt.savefig('images/O2-dissociation-sigma-convergence.png')