from vasp import Vasp
from ase import Atom, Atoms
atoms = Atoms([Atom('Cu', [0.000, 0.000, 0.000])],
              cell=[[1.818, 0.000, 1.818],
                    [1.818, 1.818, 0.000],
                    [0.000, 1.818, 1.818]])
calc = Vasp('bulk/alloy/cu',
            xc='PBE',
            encut=350,
            kpts=[13, 13, 13],
            ibrion=2,
            isif=4,
            nsw=10,
            atoms=atoms)
calc.set_nbands(f=7)
calc.write_input()  # you have to write out the input for it to take effect
print calc