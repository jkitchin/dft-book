from vasp import Vasp
from vasp.VaspChargeDensity import VaspChargeDensity
import numpy as np
from ase.units import Debye
import os
calc = Vasp('molecules/co-centered')
atoms = calc.get_atoms()
calc.stop_if(atoms.get_potential_energy() is None)
vcd = VaspChargeDensity('molecules/co-centered/CHG')
cd = np.array(vcd.chg[0])
n0, n1, n2 = cd.shape
s0 = 1.0 / n0
s1 = 1.0 / n1
s2 = 1.0 / n2
X, Y, Z = np.mgrid[0.0:1.0:s0,
                   0.0:1.0:s1,
                   0.0:1.0:s2]
C = np.column_stack([X.ravel(),
                     Y.ravel(),
                     Z.ravel()])
atoms = calc.get_atoms()
uc = atoms.get_cell()
real = np.dot(C, uc)
# now convert arrays back to unitcell shape
x = np.reshape(real[:, 0], (n0, n1, n2))
y = np.reshape(real[:, 1], (n0, n1, n2))
z = np.reshape(real[:, 2], (n0, n1, n2))
nelements = n0 * n1 * n2
voxel_volume = atoms.get_volume() / nelements
total_electron_charge = -cd.sum() * voxel_volume
electron_density_center = np.array([(cd * x).sum(),
                                    (cd * y).sum(),
                                    (cd * z).sum()])
electron_density_center *= voxel_volume
electron_density_center /= total_electron_charge
electron_dipole_moment = -electron_density_center * total_electron_charge
# now the ion charge center. We only need the Zval listed in the potcar
from vasp.POTCAR import get_ZVAL
LOP = calc.get_pseudopotentials()
ppp = os.environ['VASP_PP_PATH']
zval = {}
for sym, ppath, hash in LOP:
    fullpath = os.path.join(ppp, ppath)
    z = get_ZVAL(fullpath)
    zval[sym] = z
    ion_charge_center = np.array([0.0, 0.0, 0.0])
    total_ion_charge = 0.0
for atom in atoms:
    Z = zval[atom.symbol]
    total_ion_charge += Z
    pos = atom.position
    ion_charge_center += Z * pos
ion_charge_center /= total_ion_charge
ion_dipole_moment = ion_charge_center * total_ion_charge
dipole_vector = (ion_dipole_moment + electron_dipole_moment)
dipole_moment = ((dipole_vector**2).sum())**0.5 / Debye
print('The dipole vector is {0}'.format(dipole_vector))
print('The dipole moment is {0:1.2f} Debye'.format(dipole_moment))