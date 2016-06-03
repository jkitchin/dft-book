from vasp import Vasp
from ase import Atom, Atoms
atoms = Atoms([Atom('Cu',  [0.000, 0.000, 0.000])],
              cell= [[1.818, 0.000, 1.818],
                     [1.818, 1.818, 0.000],
                     [0.000, 1.818, 1.818]])
calc = Vasp('bulk/alloy/cu',
            xc='PBE',
            encut=350,
            kpts=[13, 13, 13],
            nbands=9,
            ibrion=2,
            isif=4,
            nsw=10,
            atoms=atoms)
print(calc.get_valence_electrons())
print(calc.potential_energy)