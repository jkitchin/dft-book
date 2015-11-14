from jasp import *
with jasp('bulk/Fe-bulk') as calc:
    calc.clone('bulk/Fe-elastic')
with jasp('bulk/Fe-elastic',
          ibrion=6,    #
          isif=3,      # gets elastic constants
          potim=0.05,  # displacements
          nsw=1,
          nfree=2) as calc:
    atoms = calc.get_atoms()
    print atoms.get_potential_energy()