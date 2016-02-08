from jasp import *
with jasp('molecules/H-beef') as calc:
    ensH = calc.get_beefens()
with jasp('molecules/H2-beef') as calc:
    ensH2 = calc.get_beefens()
ensD = 2 * ensH - ensH2
print('mean = {} eV'.format(ensD.mean()))
print('std = {} eV'.format(ensD.std()))
import matplotlib.pyplot as plt
plt.hist(ensD, 20)
plt.xlabel('Deviation')
plt.ylabel('frequency')
plt.savefig('images/beef-ens.png')