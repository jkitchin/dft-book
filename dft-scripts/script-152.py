from jasp import *
with jasp('surfaces/Al-slab-relaxed') as calc:
    atoms = calc.get_atoms()
    print calc.forces
    print atoms.get_forces(apply_constraint=False)
    print atoms.get_forces()
    print calc.forces
    print atoms.get_forces(apply_constraint=False)