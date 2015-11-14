from jasp import *
with jasp('bulk/tio2/step3') as calc:
    atoms = calc.get_atoms()
    print 'default ismear: ', atoms.get_potential_energy()
    calc.clone('bulk/tio2/step4')
with jasp('bulk/tio2/step4',
          ismear=-5,
          nsw=0) as calc:
    atoms = calc.get_atoms()
    print 'ismear=-5:      ', atoms.get_potential_energy()