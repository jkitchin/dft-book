from ase import Atoms, Atom
from jasp import *
import numpy as np
np.set_printoptions(precision=3, suppress=True)
co = Atoms([Atom('C',[0,   0, 0]),
            Atom('O',[1.2, 0, 0])],
            cell=(6., 6., 6.))
with jasp('molecules/simple-co', #output dir
          xc='PBE',  # the exchange-correlation functional
          nbands=6,  # number of bands
          encut=350, # planewave cutoff
          ismear=1,  # Methfessel-Paxton smearing
          sigma=0.01,# very small smearing factor for a molecule
          atoms=co) as calc:
    print 'energy = {0} eV'.format(co.get_potential_energy())
    print co.get_forces()