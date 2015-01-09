from jasp import *
import matplotlib.pyplot as plt
with jasp('surfaces/Al-slab-relaxed') as calc:
    atoms = calc.get_atoms()
with jasp('surfaces/Al-slab-locpot',
          xc='PBE',
          kpts=(6, 6, 1),
          encut=350,
          lvtot=True,  # write out local potential
          lvhar=True,  # write out only electrostatic potential, not xc pot
          atoms=atoms) as calc:
    calc.calculate()
    ef = calc.get_fermi_level()
    atoms = calc.get_atoms()
    x, y, z, lp = calc.get_local_potential()
nx, ny, nz = lp.shape
axy = np.array([np.average(lp[:, :, z]) for z in range(nz)])
# setup the x-axis in realspace
uc = atoms.get_cell()
xaxis = np.linspace(0, uc[2][2], nz)
plt.plot(xaxis, axy)
plt.plot([min(xaxis), max(xaxis)], [ef, ef], 'k:')
plt.xlabel('Position along z-axis')
plt.ylabel('x-y averaged electrostatic potential')
plt.savefig('images/Al-wf.png')
ind = (xaxis > 0) & (xaxis < 5)
wf = np.average(axy[ind]) - ef
print ' The workfunction is {0:1.2f} eV'.format(wf)