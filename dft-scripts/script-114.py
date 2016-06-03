from vasp import Vasp
calc = Vasp('bulk/tio2/step3')
atoms = calc.get_atoms()
print 'default ismear: ', atoms.get_potential_energy()
calc.clone('bulk/tio2/step4')
calc.set(ismear=-5,
         nsw=0)
atoms = calc.get_atoms()
print 'ismear=-5:      ', atoms.get_potential_energy()