from vasp import Vasp
from ase.dft import DOS
calc = Vasp('bulk/pd-dos')
calc.clone('bulk/pd-dos-ismear-5')
bulk = calc.get_atoms()
calc.set(ismear=-5)
bulk.get_potential_energy()
dos = DOS(calc, width=0.2)
d = dos.get_dos()
e = dos.get_energies()
import pylab as plt
plt.plot(e, d)
plt.xlabel('energy [eV]')
plt.ylabel('DOS')
plt.savefig('images/pd-dos-ismear-5.png')