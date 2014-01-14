from ase.data.molecules import molecule
from ase.io import write
atoms = molecule('CH3CN')
atoms.center(vacuum=6)
print 'unit cell'
print '---------'
print atoms.get_cell()
write('images/ch3cn-rotated.png', atoms,
      show_unit_cell=2,rotation='45x,45y,0z')