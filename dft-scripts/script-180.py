# perform a climbing image NEB calculation
from jasp import *
with jasp('surfaces/Pt-O-fcc-hcp-neb') as calc:
    calc.clone('surfaces/Pt-O-fcc-hcp-cineb')
with jasp('surfaces/Pt-O-fcc-hcp-cineb') as calc:
    calc.set(ichain=0, lclimb=True)
    images, energies = calc.get_neb(npi=4)
    calc.plot_neb(show=False)
import matplotlib.pyplot as plt
plt.savefig('images/pt-o-cineb.svg')
plt.show()