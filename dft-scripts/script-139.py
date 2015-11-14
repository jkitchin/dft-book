from jasp import *
from ase.dft import DOS
with jasp('bulk/pd-dos') as calc:
    calc.clone('bulk/pd-dos-ismear-5')
with jasp('bulk/pd-dos-ismear-5') as calc:
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