from jasp import *
from ase.dft.stm import STM
import matplotlib.pyplot as plt
with jasp('surfaces/Al-slab-relaxed') as calc:
    atoms = calc.get_atoms()
    stm = STM(atoms)
    z = 8.0
    bias = 1.0
    c = stm.get_averaged_current(bias, z)
    x, y, h = stm.scan(bias, c, repeat=(3, 5))
    plt.gca(aspect='equal')
    plt.contourf(x, y, h, 40)
    plt.hot()
    plt.colorbar()
    plt.show()