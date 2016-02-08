from jasp import *
with jasp('surfaces/Al-slab-relaxed') as calc:
    atoms = calc.get_atoms()
    print 'Constraints = True: ', atoms.get_forces(apply_constraint=True)
    print 'Constraints = False: ', atoms.get_forces(apply_constraint=False)