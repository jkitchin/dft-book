from ase.structure import molecule
print 'linear rotors: I = [0 Ia Ia]'
atoms = molecule('CO2')
print '  CO2 moments of inertia: ',atoms.get_moments_of_inertia()
print
print 'symmetric rotors (Ia = Ib) < Ic'
atoms = molecule('NH3')
print '  NH3 moments of inertia: ' ,atoms.get_moments_of_inertia()
atoms = molecule('C6H6')
print '  C6H6 moments of inertia:' ,atoms.get_moments_of_inertia()
print
print 'symmetric rotors Ia < (Ib = Ic)'
atoms = molecule('CH3Cl')
print 'CH3Cl moments of inertia: ',atoms.get_moments_of_inertia()
print
print 'spherical rotors Ia = Ib = Ic'
atoms = molecule('CH4')
print '  CH4 moments of inertia: ' ,atoms.get_moments_of_inertia()
print
print 'unsymmetric rotors Ia != Ib != Ic'
atoms = molecule('C3H7Cl')
print '  C3H7Cl moments of inertia: ' ,atoms.get_moments_of_inertia()