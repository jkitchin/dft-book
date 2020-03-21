from vasp import Vasp
calc = Vasp('bulk/Fe-bulk')
calc.clone('bulk/Fe-elastic')
calc.set(ibrion=6,    #
         isif=3,      # gets elastic constants
         potim=0.05,  # displacements
         nsw=1,
         nfree=2)
print(calc.potential_energy)