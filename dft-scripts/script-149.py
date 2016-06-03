from vasp import Vasp
from ase.dft import DOS
# This seems very slow...
calc = Vasp('bulk/pd-dos-k20-ismear-5')
print DOS(calc, width=0.2)