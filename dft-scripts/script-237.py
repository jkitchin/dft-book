import numpy as np
from Scientific.Geometry import Vector
A = Vector([1,1,1])   #Scientfic
a = np.array([1,1,1]) #numpy
B = Vector([0.0,1.0,0.0])
print '|A| = ',A.length()        #Scientific Python way
print '|a| = ',np.sum(a**2)**0.5 #numpy way
print '|a| = ',np.linalg.norm(a) #numpy way 2
print 'ScientificPython angle = ',A.angle(B) #in radians
print 'numpy angle =            ',np.arccos(np.dot(a/np.linalg.norm(a),B/np.linalg.norm(B)))
#cross products
print 'Scientific A .cross. B = ',A.cross(B)
print 'numpy A .cross. B      = ',np.cross(A,B) #you can use Vectors in numpy