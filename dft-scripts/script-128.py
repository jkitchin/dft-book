# run CuO calculation
from jasp import *
from ase import Atom, Atoms
# CuO
# http://cst-www.nrl.navy.mil/lattice/struk/b26.html
# http://www.springermaterials.com/docs/info/10681727_51.html
a = 4.6837
b = 3.4226
c = 5.1288
beta = 99.54/180*np.pi
y = 0.5819
a1 = np.array([0.5*a, -0.5*b, 0.0])
a2 = np.array([0.5*a, 0.5*b, 0.0])
a3 = np.array([c*np.cos(beta), 0.0, c*np.sin(beta)])
atoms = Atoms([Atom('Cu', 0.5*a2),
               Atom('Cu', 0.5*a1 + 0.5*a3),
               Atom('O', -y*a1 + y*a2 + 0.25*a3),
               Atom('O',  y*a1 - y*a2 - 0.25*a3)],
               cell=(a1, a2, a3))
with jasp('bulk/CuO',
          encut=400,
          kpts=(8,8,8),
          ibrion=2,
          isif=3,
          nsw=30,
          xc='PBE',
          atoms=atoms) as calc:
    calc.set_nbands()
    calc.calculate()
    print calc