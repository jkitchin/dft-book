from vasp import Vasp
import matplotlib.pyplot as plt
from ase.dft import DOS
calc = Vasp('bulk/pd-dos')
dos = DOS(calc, width=0.2)
d = dos.get_dos()
e = dos.get_energies()
import pylab as plt
plt.plot(e, d)
plt.xlabel('energy (eV)')
plt.ylabel('DOS')
plt.savefig('images/pd-dos.png')