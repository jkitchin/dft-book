from jasp import *
from jasp.elastic_moduli import *
with jasp('bulk/Al-bulk') as calc:
    calc.clone('bulk/Al-elastic')
with jasp('bulk/Al-elastic',
          ibrion=6,    #
          isif=3,      # gets elastic constants
          potim=0.015,  # displacements
          nsw=1,
          nfree=2) as calc:
    atoms = calc.get_atoms()
    print atoms.get_potential_energy() 
    EM = calc.get_elastic_moduli()
    print EM
c11 = EM[0,0]
c12 = EM[0,1]
B = (c11 + 2 * c12) / 3.0
print B