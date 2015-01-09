from jasp import *
import matplotlib.pyplot as plt
with jasp('surfaces/Al-Na-nodip') as calc:
    atoms = calc.get_atoms()
    x, y, z, lp = calc.get_local_potential()
    nx, ny, nz = lp.shape
    axy_1 = [np.average(lp[:, :, z]) for z in range(nz)]
    # setup the x-axis in realspace
    uc = atoms.get_cell()
    xaxis_1 = np.linspace(0, uc[2][2], nz)
    e1 = atoms.get_potential_energy()
with jasp('surfaces/Al-Na-dip-step2') as calc:
    atoms = calc.get_atoms()
    x, y, z, lp = calc.get_local_potential()
    nx, ny, nz = lp.shape
    axy_2 = [np.average(lp[:, :, z]) for z in range(nz)]
    # setup the x-axis in realspace
    uc = atoms.get_cell()
    xaxis_2 = np.linspace(0, uc[2][2], nz)
    ef2 = calc.get_fermi_level()
    e2 = atoms.get_potential_energy()
print 'The difference in energy is {0} eV.'.format(e2-e1)
plt.plot(xaxis_1, axy_1, label='no dipole correction')
plt.plot(xaxis_2, axy_2, label='dipole correction')
plt.plot([min(xaxis_2), max(xaxis_2)], [ef2, ef2], 'k:', label='Fermi level')
plt.xlabel('z ($\AA$)')
plt.ylabel('xy-averaged electrostatic potential')
plt.legend(loc='best')
plt.savefig('images/dip-vs-nodip-esp.png')