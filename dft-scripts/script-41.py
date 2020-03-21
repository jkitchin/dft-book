from vasp import Vasp
bond_lengths = [1.05, 1.1, 1.15, 1.2, 1.25]
calcs = [Vasp('molecules/co-{0}'.format(d)) for d in bond_lengths]
energies = [calc.get_atoms().get_potential_energy() for calc in calcs]
print(energies)