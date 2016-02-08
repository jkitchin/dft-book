from jasp import *
from ase.dft.dos import *
with jasp('molecules/O2-sp-triplet') as calc:
    dos = DOS(calc, width=0.2)
    d_up = dos.get_dos(spin=0)
    d_down = dos.get_dos(spin=1)
    e = dos.get_energies()
ind = e <= 0.0
# integrate up to 0eV
print('number of up states = {0}'.format(np.trapz(d_up[ind], e[ind])))
print('number of down states = {0}'.format(np.trapz(d_down[ind], e[ind])))
import pylab as plt
plt.plot(e, d_up,
         e, -d_down)
plt.xlabel('energy [eV]')
plt.ylabel('DOS')
plt.legend(['up', 'down'])
plt.savefig('images/O2-sp-dos.png')