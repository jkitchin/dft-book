from vasp import Vasp
calc = Vasp('molecules/H-beef')
ensH = calc.get_beefens()
calc = Vasp('molecules/H2-beef')
ensH2 = calc.get_beefens()
ensD = 2 * ensH - ensH2
print('mean = {} eV'.format(ensD.mean()))
print('std = {} eV'.format(ensD.std()))
import matplotlib.pyplot as plt
plt.hist(ensD, 20)
plt.xlabel('Deviation')
plt.ylabel('frequency')
plt.savefig('images/beef-ens.png')