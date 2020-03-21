# make neb movie
from ase.io import write
from ase.visualize import view
from vasp import Vasp
calc = Fasp('molecules/nh3-neb') as calc:
images, energies = calc.get_neb()
# this rotates the atoms 90 degrees about the y-axis
[atoms.rotate('y', np.pi/2.) for atoms in images]
for i,atoms in enumerate(images):
    write('images/00{0}-nh3.png'.format(i), atoms, show_unit_cell=2)
# animated gif
os.system('convert -delay 50 -loop 0 images/00*-nh3.png images/nh3-neb.gif')
# Shockwave flash
os.system('png2swf -o images/nh3-neb.swf images/00*-nh3.png ')