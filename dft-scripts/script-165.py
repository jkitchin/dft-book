from ase.lattice.surface import surface
from ase.io import write
# Au(211) with 9 layers
s1 = surface('Au', (2, 1, 1), 9)
s1.center(vacuum=10, axis=2)
write('images/Au-211.png',
      s1.repeat((3, 3, 1)),
      rotation='-30z,90x',  # change the orientation for viewing
      show_unit_cell=2)