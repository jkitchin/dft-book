from vasp import Vasp
calc = Vasp('surfaces/Al-slab-relaxed')
atoms = calc.get_atoms()
print('Constraints = True: ', atoms.get_forces(apply_constraint=True))
print('Constraints = False: ', atoms.get_forces(apply_constraint=False))