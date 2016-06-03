from vasp import Vasp
npoints = 200
width = 0.5
def gaussian(energies, eik):
    x = ((energies - eik) / width)
    return np.exp(-x**2) / np.sqrt(np.pi) / width
calc = Vasp('bulk/pd-dos')
# kpt weights
wk = calc.get_k_point_weights()
# for each k-point there are a series of eigenvalues
# here we get all the eigenvalues for each k-point
e_kn = []
for i, k in enumerate(wk):
    e_kn.append(calc.get_eigenvalues(kpt=i))
e_kn = np.array(e_kn) - calc.get_fermi_level()
# these are the energies we want to evaluate the dos at
energies = np.linspace(e_kn.min(), e_kn.max(), npoints)
# this is where we build up the dos
dos = np.zeros(npoints)
for j in range(npoints):
    for k in range(len(wk)): # loop over all kpoints
        for i in range(len(e_kn[k])): # loop over eigenvalues in each k
            dos[j] += wk[k] * gaussian(energies[j], e_kn[k][i])
import matplotlib.pyplot as plt
plt.plot(energies, dos)
plt.savefig('images/manual-dos.png')
plt.show()