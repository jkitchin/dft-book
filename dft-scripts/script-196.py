from jasp import *
from ase.lattice.cubic import FaceCenteredCubic
from ase.dft import DOS
atoms = FaceCenteredCubic(directions=[[0,1,1],
                                      [1,0,1],
                                      [1,1,0]],
                                      size=(1,1,1),
                                      symbol='Ni')
atoms[0].magmom = 1
with jasp('bulk/Ni-PBE',
          ismear=-5,
          kpts=(5,5,5),
          xc='PBE',
          ispin=2,lorbit=11,
          atoms=atoms) as calc:
    print 'PBE energy:   ',atoms.get_potential_energy()
    dos = DOS(calc, width=0.2)
    e_pbe = dos.get_energies()
    d_pbe = dos.get_dos()
    calc.clone('bulk/Ni-PBE0')
    calc.clone('bulk/Ni-HSE06')
with jasp('bulk/Ni-PBE0') as calc:
     calc.set(lhfcalc=True,
              algo='D',
              time=0.4)
     atoms = calc.get_atoms()
     print 'PBE0 energy:  ',atoms.get_potential_energy()
     dos = DOS(calc, width=0.2)
     e_pbe0 = dos.get_energies()
     d_pbe0 = dos.get_dos()
with jasp('bulk/Ni-HSE06') as calc:
     calc.set(lhfcalc=True,
              hfscreen=0.2,
              algo='D', time=0.4)
     atoms = calc.get_atoms()
     print 'HSE06 energy: ', atoms.get_potential_energy()
     dos = DOS(calc, width=0.2)
     e_hse06 = dos.get_energies()
     d_hse06 = dos.get_dos()
import pylab as plt
plt.plot(e_pbe, d_pbe, label='PBE')
plt.plot(e_pbe0, d_pbe0, label='PBE0')
plt.plot(e_hse06, d_hse06, label='HSE06')
plt.xlabel('energy [eV]')
plt.ylabel('DOS')
plt.legend()
plt.savefig('images/ni-dos-pbe-pbe0-hse06.png')