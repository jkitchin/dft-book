from jasp import *
from ase.dft.dos import DOS
import matplotlib.pyplot as plt
# get the geometry from another calculation
with jasp('molecules/simple-co') as calc:
    atoms = calc.get_atoms()
with jasp('molecules/co-ados',
          encut=300,
          xc='PBE',
          rwigs=[1.0, 1.0],     # these are the cutoff radii for projected states
          atoms=atoms) as calc:
    calc.calculate()
    # now get results
    dos = DOS(calc)
    plt.plot(dos.get_energies(), dos.get_dos() + 10)
    ados = VaspDos(efermi=calc.get_fermi_level())
    energies = ados.energy
    plt.plot(energies, ados.dos + 8, label='ADOS')  # these are the total DOS
    c_s = ados.site_dos(0, 's')
    c_p = ados.site_dos(0, 'p')
    o_s = ados.site_dos(1, 's')
    o_p = ados.site_dos(1, 'p')
    c_d = ados.site_dos(0, 'd')
    o_d = ados.site_dos(1, 'd')
    plt.plot(energies, c_s + 6, energies, o_s + 5)
    plt.plot(energies, c_p + 4, energies, o_p + 3)
    plt.plot(energies, c_d, energies, o_d + 2)
    plt.xlabel('Energy - $E_f$ (eV)')
    plt.ylabel('DOS')
    plt.legend(['DOS', 'ADOS',
                'C$_s$', 'O$_s$',
                'C$_p$', 'O$_p$',
                'C$_d$', 'O$_d$'],
                 ncol=2, loc='best')
plt.savefig('images/co-ados.png')