from vasp import Vasp
calc = Vasp('molecules/h2o-relax-centered')
from ase.visualize import view
view(calc.traj)