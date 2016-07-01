# perform a climbing image NEB calculation
from vasp import Vasp
calc = Vasp('surfaces/Pt-O-fcc-hcp-neb')
calc.clone('surfaces/Pt-O-fcc-hcp-cineb')
calc.set(ichain=0, lclimb=True)
images, energies = calc.get_neb()
calc.plot_neb(show=False)
import matplotlib.pyplot as plt
plt.savefig('images/pt-o-cineb.svg')
plt.show()