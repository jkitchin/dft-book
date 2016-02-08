from jasp import *
from ase.neb import NEB
import matplotlib.pyplot as plt
with jasp('surfaces/Pt-slab-O-fcc') as calc:
    initial_atoms = calc.get_atoms()
with jasp('surfaces/Pt-slab-O-hcp') as calc:
    final_atoms = calc.get_atoms()
# here is our estimated transition state. we use vector geometry to
# define the bridge position, and add 1.451 Ang to z based on our
# previous bridge calculation. The bridge position is half way between
# atoms 9 and 10.
ts = initial_atoms.copy()
ts.positions[-1] = 0.5 * (ts.positions[9] + ts.positions[10]) + [0, 0, 1.451]
# construct the band
images = [initial_atoms]
images += [initial_atoms.copy()]
images += [ts.copy()]  # this is the TS
neb = NEB(images)
# Interpolate linearly the positions of these images:
neb.interpolate()
# now add the second half
images2 = [ts.copy()]
images2 += [ts.copy()]
images2 += [final_atoms]
neb2 = NEB(images2)
neb2.interpolate()
# collect final band. Note we do not repeat the TS in the second half
final_images = images + images2[1:]
with jasp('surfaces/Pt-O-fcc-hcp-neb',
          ibrion=1,
          nsw=90,
          spring=-5,
          atoms=final_images) as calc:
    try:
        images, energies = calc.get_neb()
        p = calc.plot_neb(show=False)
        # remember you are in surfaces/Pt-O-fcc-hcp-neb, so to save in
        # the images directory you need ../../ in the path to get you
        # back up.
        plt.savefig('../../images/pt-o-fcc-hcp-neb.png')
    except (VaspSubmitted, VaspQueued):
        pass