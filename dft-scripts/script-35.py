from vasp import Vasp
from ase.dft.dos import DOS
import matplotlib.pyplot as plt
# get the geometry from another calculation
calc = Vasp('molecules/simple-co')
atoms = calc.get_atoms()
calc = Vasp('molecules/co-ados',
            encut=300,
            xc='PBE',
            rwigs={'C': 1.0, 'O': 1.0},     # these are the cutoff radii for projected states
            atoms=atoms)
calc.stop_if(calc.potential_energy is None)
# now get results
dos = DOS(calc)
plt.plot(dos.get_energies(), dos.get_dos() + 10)
energies, c_s = calc.get_ados(0, 's')
_, c_p = calc.get_ados(0, 'p')
_, o_s = calc.get_ados(1, 's')
_, o_p = calc.get_ados(1, 'p')
_, c_d = calc.get_ados(0, 'd')
_, o_d = calc.get_ados(1, 'd')
plt.plot(energies, c_s + 6, energies, o_s + 5)
plt.plot(energies, c_p + 4, energies, o_p + 3)
plt.plot(energies, c_d, energies, o_d + 2)
plt.xlabel('Energy - $E_f$ (eV)')
plt.ylabel('DOS')
plt.legend(['DOS',
            'C$_s$', 'O$_s$',
            'C$_p$', 'O$_p$',
            'C$_d$', 'O$_d$'],
           ncol=2, loc='best')
plt.savefig('images/co-ados.png')