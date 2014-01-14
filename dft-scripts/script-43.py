from jasp import *
import numpy as np
with jasp('molecules/h2o_vib') as calc:
    energies, modes = calc.get_vibrational_modes(mode=3, massweighted=True,
                                                 show=True)