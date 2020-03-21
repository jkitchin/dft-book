# <<h2o-vib-vis>>
from vasp import Vasp
import numpy as np
calc = Vasp('molecules/h2o_vib')
energies, modes = calc.get_vibrational_modes(mode=0, massweighted=True,
                                             show=True)