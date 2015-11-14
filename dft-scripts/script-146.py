f = open('bulk/Si-bandstructure/EIGENVAL', 'r')
line1 = f.readline()
line2 = f.readline()
line3 = f.readline()
line4 = f.readline()
comment = f.readline()
unknown, nkpoints, nbands = [int(x) for x in f.readline().split()]
blankline = f.readline()
band_energies = [[] for i in range(nbands)]
for i in range(nkpoints):
    x, y, z, weight = [float(x) for x in f.readline().split()]
    for j in range(nbands):
        fields = f.readline().split()
        id, energy = int(fields[0]), float(fields[1])
        band_energies[id - 1].append(energy)
    blankline = f.readline()
f.close()
import matplotlib.pyplot as plt
for i in range(nbands):
    plt.plot(range(nkpoints), band_energies[i])
ax = plt.gca()
ax.set_xticks([]) # no tick marks
plt.xlabel('k-vector')
plt.ylabel('Energy (eV)')
ax.set_xticks([0, 10, 19])
ax.set_xticklabels(['$L$', '$\Gamma$', '$X$'])
plt.savefig('images/Si-bandstructure.png')