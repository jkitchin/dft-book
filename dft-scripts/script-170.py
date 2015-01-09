# compute local potential with dipole calculation on
from ase.lattice.surface import fcc111, add_adsorbate
from jasp import *
slab = fcc111('Al', size=(2, 2, 2), vacuum=10.0)
add_adsorbate(slab, 'Na', height=1.2, position='fcc')
slab.center()
with jasp('surfaces/Al-Na-dip',
          xc='PBE',
          encut=340,
          kpts=(2, 2, 1),
          idipol=3,   # only along z-axis
          lvtot=True,  # write out local potential
          lvhar=True,  # write out only electrostatic potential, not xc pot
          atoms=slab) as calc:
    calc.calculate()
    x, y, z, cd = calc.get_charge_density()
    n0, n1, n2 = cd.shape
    nelements = n0 * n1 * n2
    voxel_volume = slab.get_volume() / nelements
    total_electron_charge = cd.sum() * voxel_volume
    electron_density_center = np.array([(cd * x).sum(),
                                        (cd * y).sum(),
                                        (cd * z).sum()])
    electron_density_center *= voxel_volume
    electron_density_center /= total_electron_charge
    print 'electron-density center = {0}'.format(electron_density_center)
    uc = slab.get_cell()
    # get scaled electron charge density center
    sedc = np.dot(np.linalg.inv(uc.T), electron_density_center.T).T
    # we only write 4 decimal places out to the INCAR file, so we round here.
    sedc = np.round(sedc, 4)
    calc.clone('surfaces/Al-Na-dip-step2')
# now run step 2 with dipole set at scaled electron charge density center
with jasp('surfaces/Al-Na-dip-step2',
           ldipol=True, dipol=sedc) as calc:
    calc.calculate()