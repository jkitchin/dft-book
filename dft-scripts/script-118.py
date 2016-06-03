#+BEGIN_SRC python
from vasp import Vasp
calc = Vasp('bulk/Al-lda-vasp')
calc.view()
print [atoms.get_volume() for atoms in calc.traj]
print [atoms.get_potential_energy() for atoms in calc.traj]