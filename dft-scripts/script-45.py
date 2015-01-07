from jasp import *
import numpy as np
c = 3e10  # speed of light cm/s
h = 4.135667516e-15  # eV/s
# first, get the frequencies.
with jasp('molecules/h2o_vib') as calc:
    freq = calc.get_vibrational_frequencies()
ZPE = 0.0
for f in freq:
    if not isinstance(f, float):
        continue  # skip complex numbers
    nu = f * c  # convert to frequency
    ZPE += 0.5 * h * nu
print 'The ZPE of water is {0:1.3f} eV'.format(ZPE)
# one liner
ZPE = np.sum([0.5 * h * f * c for f in freq if isinstance(f, float)])
print 'The ZPE of water is {0:1.3f} eV'.format(ZPE)