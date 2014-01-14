from jasp import *
from ase.lattice.cubic import BodyCenteredCubic
atoms = BodyCenteredCubic(directions=[[1,0,0],
                                      [0,1,0],
                                      [0,0,1]],
                                      size=(1,1,1),
                                      symbol='Fe')
NUPDOWNS = [0.0, 2.0, 4.0, 5.0, 6.0, 8.0]
energies = []
for B in NUPDOWNS:
    with jasp('bulk/Fe-bcc-fixedmagmom-{0:1.2f}'.format(B),
          xc='PBE',
          encut=300,
          kpts=(4,4,4),
          ispin=2,
          nupdown=B,
          atoms=atoms) as calc:
        try:
            e = atoms.get_potential_energy()
            energies.append(e)
        except (VaspSubmitted, VaspQueued):
            pass
import matplotlib.pyplot as plt
plt.plot(NUPDOWNS, energies)
plt.xlabel('Total Magnetic Moment')
plt.ylabel('Energy (eV)')
plt.savefig('images/Fe-fixedmagmom.png')