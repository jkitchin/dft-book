from jasp import *
with jasp('surfaces/Pt-slab-O-fcc') as calc:
    calc.clone('Pt-slab-O-fcc-vib-ibrion=6')
with jasp('surfaces/Pt-slab-O-fcc-vib-ibrion=6') as calc:
    calc.set(ibrion=6,# finite differences with symmetry
             nfree=2, # central differences (default)
             potim=0.015,# default as well
             ediff=1e-8,
             nsw=1)
    atoms = calc.get_atoms()
    print 'Elapsed time = {0} seconds'.format(calc.get_elapsed_time())
    f,m = calc.get_vibrational_modes(0)
    allfreq = calc.get_vibrational_modes()[0]
from ase.units import meV
c = 3e10 # cm/s
h = 4.135667516e-15 # eV*s
print 'For mode 0:'
print 'vibrational energy = {0} eV'.format(f)
print 'vibrational energy = {0} meV'.format(f/meV)
print 'vibrational freq   = {0} 1/s'.format(f/h)
print 'vibrational freq   = {0} cm^{{-1}}'.format(f/(h*c))
print
print 'All energies = ',allfreq