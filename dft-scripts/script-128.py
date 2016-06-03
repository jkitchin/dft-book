from vasp import Vasp
calc = Vasp('bulk/Al-bulk')
calc.clone('bulk/Al-elastic')
calc.set(ibrion=6,    #
         isif=3,      # gets elastic constants
         potim=0.015,  # displacements
         nsw=1,
         nfree=2)
calc.wait(abort=True)
EM = calc.get_elastic_moduli()
print(EM)
c11 = EM[0, 0]
c12 = EM[0, 1]
B = (c11 + 2 * c12) / 3.0
print(B)