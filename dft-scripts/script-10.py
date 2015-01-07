from ase.structure import molecule
from ase.io import write
from numpy import pi
atoms = molecule('CH3CN')
atoms.center(vacuum=6)
p1 = atoms.get_positions()
atoms.rotate('x', pi/4, center='COM', rotate_cell=False)
atoms.rotate('y', pi/4, center='COM', rotate_cell=False)
write('images/ch3cn-rotated-2.png', atoms, show_unit_cell=2)
print 'difference in positions after rotating'
print 'atom    difference vector'
print '--------------------------------------'
p2 = atoms.get_positions()
diff = p2 - p1
for i, d in enumerate(diff):
    print '{0} {1}'.format(i, d)