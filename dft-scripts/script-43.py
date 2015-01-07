# <<water-vib>>
# adapted from http://cms.mpi.univie.ac.at/wiki/index.php/H2O_vibration
from ase import Atoms, Atom
from jasp import *
import ase.units
atoms = Atoms([Atom('H', [0.5960812,  -0.7677068,   0.0000000]),
               Atom('O', [0.0000000,   0.0000000,   0.0000000]),
               Atom('H', [0.5960812,   0.7677068,   0.0000000])],
               cell=(8, 8, 8))
atoms.center()
with jasp('molecules/h2o_vib',
          xc='PBE',
          encut=400,
          ismear=0,     # Gaussian smearing
          ibrion=6,     # finite differences with symmetry
          nfree=2,      # central differences (default)
          potim=0.015,  # default as well
          ediff=1e-8,   # for vibrations you need precise energies
          nsw=1,        # Set to 1 for vibrational calculation
          atoms=atoms) as calc:
    print 'Forces'
    print '======'
    print atoms.get_forces()
    print
    # vibrational energies are in eV
    energies, modes = calc.get_vibrational_modes()
    print 'energies\n========'
    for i, e in enumerate(energies):
        print '{0:02d}: {1} eV'.format(i, e)