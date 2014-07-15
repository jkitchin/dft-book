from jasp import *
from ase.dft.dos import DOS
import matplotlib.pyplot as plt
with jasp('molecules/simple-co') as calc: # we already ran this!
    dos = DOS(calc)
    plt.plot(dos.get_energies(), dos.get_dos())
    plt.xlabel('Energy - $E_f$ (eV)')
    plt.ylabel('DOS')
# make sure you save the figure outside the with statement, or provide
# the correct relative or absolute path to where you want it.
plt.savefig('images/co-dos.png')