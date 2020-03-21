from vasp import Vasp
calc = Vasp('bulk/tio2/step1-0.90')
calc.clone('bulk/tio2/step2-0.90')
#calc.set(isif=4)
print calc.set(isif=4)
print calc.calculation_required()