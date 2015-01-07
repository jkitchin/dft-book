from ase.structure import molecule
from ase.io import write
atoms1 = molecule('NH3')
atoms2 = molecule('O2')
atoms2.translate([3, 0, 0])
bothatoms = atoms1 + atoms2
bothatoms.center(5)
write('images/bothatoms.png', bothatoms, show_unit_cell=2, rotation='90x')