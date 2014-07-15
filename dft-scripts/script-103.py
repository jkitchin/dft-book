from jasp import *
with jasp('bulk/tio2/step2-1.05') as calc:
    calc.clone('bulk/tio2/step3')
with jasp('bulk/tio2/step3',
          isif=3) as calc:
    calc.calculate()
    atoms = calc.get_atoms()
    print calc
from pyspglib import spglib
print '\nThe spacegroup is {0}'.format(spglib.get_spacegroup(atoms))