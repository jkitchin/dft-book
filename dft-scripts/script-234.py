from vasp import Vasp
from ase.structure import molecule
import matplotlib.pyplot as plt
H2 = molecule('H2')
H2.set_cell([8, 8, 8], scale_atoms=False)
H2.center()
calc = Vasp('molecules/H2-beef',
          xc='beef-vdw',
            encut=350,
            ismear=0,
            ibrion=2,
            nsw=10,
            atoms=H2)
eH2 = H2.get_potential_energy()
print(eH2)