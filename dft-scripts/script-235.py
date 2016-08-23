from vasp import Vasp
from ase.structure import molecule
H = molecule('H')
H.set_cell([8, 8, 8], scale_atoms=False)
H.center()
calc = Vasp('molecules/H-beef',
            xc='beef-vdw',
            encut=350,
            ismear=0,
            atoms=H)
print(calc.potential_energy)