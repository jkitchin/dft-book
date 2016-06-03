from ase import Atoms, Atom
from vasp import Vasp
from vasp.vasprc import VASPRC
VASPRC['queue.ppn'] = 4
co = Atoms([Atom('C', [0, 0, 0]),
            Atom('O', [1.2, 0, 0])],
           cell=(6., 6., 6.))
calc = Vasp('molecules/simple-co-n4',  # output dir
            xc='PBE',  # the exchange-correlation functional
            nbands=6,    # number of bands
            encut=350,    # planewave cutoff
            ismear=1,    # Methfessel-Paxton smearing
            sigma=0.01,  # very small smearing factor for a molecule
            atoms=co)
print('energy = {0} eV'.format(co.get_potential_energy()))
print(co.get_forces())