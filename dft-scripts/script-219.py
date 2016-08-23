from vasp import Vasp
from ase.lattice.cubic import FaceCenteredCubic
from ase.dft import DOS
atoms = FaceCenteredCubic(directions=[[0, 1, 1],
                                      [1, 0, 1],
                                      [1, 1, 0]],
                                      size=(1, 1, 1),
                                      symbol='Ni')
atoms[0].magmom = 1
calc = Vasp('bulk/Ni-PBE',
            ismear=-5,
            kpts=[5, 5, 5],
            xc='PBE',
            ispin=2,
            lorbit=11,
            lwave=True, lcharg=True,  # store for reuse
            atoms=atoms)
e = atoms.get_potential_energy()
print('PBE energy:   ',e)
calc.stop_if(e is None)
dos = DOS(calc, width=0.2)
e_pbe = dos.get_energies()
d_pbe = dos.get_dos()
calc.clone('bulk/Ni-PBE0')
calc.set(xc='pbe0')
atoms = calc.get_atoms()
pbe0_e = atoms.get_potential_energy()
if atoms.get_potential_energy() is not None:
    dos = DOS(calc, width=0.2)
    e_pbe0 = dos.get_energies()
    d_pbe0 = dos.get_dos()
## HSE06
calc = Vasp('bulk/Ni-PBE')
calc.clone('bulk/Ni-HSE06')
calc.set(xc='hse06')
atoms = calc.get_atoms()
hse06_e = atoms.get_potential_energy()
if hse06_e is not None:
    dos = DOS(calc, width=0.2)
    e_hse06 = dos.get_energies()
    d_hse06 = dos.get_dos()
calc.stop_if(None in [e, pbe0_e, hse06_e])
import pylab as plt
plt.plot(e_pbe, d_pbe, label='PBE')
plt.plot(e_pbe0, d_pbe0, label='PBE0')
plt.plot(e_hse06, d_hse06, label='HSE06')
plt.xlabel('energy [eV]')
plt.ylabel('DOS')
plt.legend()
plt.savefig('images/ni-dos-pbe-pbe0-hse06.png')