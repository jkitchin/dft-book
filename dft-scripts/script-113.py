from vasp import Vasp
calc = Vasp('bulk/tio2/step2-1.05')
calc.clone('bulk/tio2/step3')
calc = Vasp('bulk/tio2/step3',
            isif=3)
calc.wait()
print calc
from pyspglib import spglib
print '\nThe spacegroup is {0}'.format(spglib.get_spacegroup(calc.atoms))