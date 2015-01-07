import numpy as np
from ase.lattice.cubic import FaceCenteredCubic
ag = FaceCenteredCubic(directions=[[1,0,0],
                                   [0,1,0],
                                   [0,0,1]],
                       size=(1,1,1),
                       symbol='Ag',
                       latticeconstant=4.0)
# these are the reciprocal lattice vectors
b1,b2,b3 = np.linalg.inv(ag.get_cell())
'''
g(111) = 1*b1 + 1*b2 + 1*b3
and |g(111)| = 1/d_111
'''
h,k,l = (1,1,1)
d = 1./np.linalg.norm(h*b1 + k*b2 + l*b3)
print 'd_111 spacing (method 1) = {0:1.3f} Angstroms'.format(d)
#method #2
hkl = np.array([h,k,l])
G = np.array([b1,b2,b3]) #reciprocal unit cell
'''
Gstar is usually defined as this matrix of dot products:
Gstar = np.array([[dot(b1,b1), dot(b1,b2), dot(b1,b3)],
                  [dot(b1,b2), dot(b2,b2), dot(b2,b3)],
                  [dot(b1,b3), dot(b2,b3), dot(b3,b3)]])
but I prefer the notationally more compact:
Gstar = G .dot. transpose(G)
then, 1/d_hkl^2 = hkl .dot. Gstar .dot. hkl
'''
Gstar = np.dot(G,G.T)
id2 = np.dot(hkl,np.dot(Gstar,hkl))
print 'd_111 spacing (method 2) =',np.sqrt(1/id2)
# http://books.google.com/books?id=nJHSqEseuIUC&lpg=PA118&ots=YA9TBldoVH
# &dq=reciprocal%20metric%20tensor&pg=PA119#v=onepage
# &q=reciprocal%20metric%20tensor&f=false
'''Finally, many text books on crystallography use long algebraic
formulas for computing the d-spacing with sin and cos, vector lengths,
and angles. Below we compute these and use them in the general
triclinic structure formula which applies to all the structures.
'''
from Scientific.Geometry import Vector
import math
unitcell = ag.get_cell()
A = Vector(unitcell[0])
B = Vector(unitcell[1])
C = Vector(unitcell[2])
# lengths of the vectors
a = A.length()#*angstroms2bohr
b = B.length()#*angstroms2bohr
c = C.length()#*angstroms2bohr
# angles between the vectors in radians
alpha = B.angle(C)
beta = A.angle(C)
gamma = A.angle(B)
print
print 'a   b   c   alpha beta gamma'
print '{0:1.3f} {1:1.3f} {2:1.3f} {3:1.3f} {4:1.3f} {5:1.3f}\n'.format(a,b,c,
                                                                alpha,beta,gamma)
h,k,l = (1,1,1)
from math import sin, cos
id2 = ((h**2/a**2*sin(alpha)**2
       + k**2/b**2*sin(beta)**2
       + l**2/c**2*sin(gamma)**2
       +2*k*l/b/c*(cos(beta)*cos(gamma)-cos(alpha))
       +2*h*l/a/c*(cos(alpha)*cos(gamma)-cos(beta))
       +2*h*k/a/b*(cos(alpha)*cos(beta)-cos(gamma)))
       /(1-cos(alpha)**2-cos(beta)**2 - cos(gamma)**2
         +2*cos(alpha)*cos(beta)*cos(gamma)))
d = 1/math.sqrt(id2)
print 'd_111 spacing (method 3) = {0}'.format(d)