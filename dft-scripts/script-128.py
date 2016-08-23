from vasp import Vasp
from ase.lattice.cubic import FaceCenteredCubic
atoms = FaceCenteredCubic(symbol='Al')
calc = Vasp('bulk/Al-bulk',
            xc='PBE',
            kpts=[12, 12, 12],
            encut=350,
            prec='High',
            isif=3,
            nsw=30,
            ibrion=1,
            atoms=atoms)
print(calc.potential_energy)