from jasp import jasp
import numpy as np
with jasp('molecules/co-centered') as calc:
    atoms = calc.get_atoms()
    x, y, z, cd = calc.get_charge_density()
def interp3d(x,y,z,cd,xi,yi,zi):
    '''
    interpolate a cubic 3D grid defined by x,y,z,cd at the point
    (xi,yi,zi)
    '''
    def get_index(value,vector):
        '''
        assumes vector ordered decreasing to increasing. A bisection
        search would be faster.
        '''
        for i,val in enumerate(vector):
            if val > value:
                return i-1
        return None
    xv = x[:,0,0]
    yv = y[0,:,0]
    zv = z[0,0,:]
    a,b,c = xi, yi, zi
    i = get_index(a,xv)
    j = get_index(b,yv)
    k = get_index(c,zv)
    x1 = x[i,j,k]
    x2 = x[i+1,j,k]
    y1 = y[i,j,k]
    y2 = y[i,j+1,k]
    z1 = z[i,j,k]
    z2 = z[i,j,k+1]
    u1 = cd[i, j, k]
    u2 = cd[i+1, j, k]
    u3 = cd[i, j+1, k]
    u4 = cd[i+1, j+1, k]
    u5 = cd[i, j, k+1]
    u6 = cd[i+1, j, k+1]
    u7 = cd[i, j+1, k+1]
    u8 = cd[i+1, j+1, k+1]
    w1 = u2 + (u2-u1)/(x2-x1)*(a-x2)
    w2 = u4 + (u4-u3)/(x2-x1)*(a-x2)
    w3 = w2 + (w2-w1)/(y2-y1)*(b-y2)
    w4 = u5 + (u6-u5)/(x2-x1)*(a-x1)
    w5 = u7 + (u8-u7)/(x2-x1)*(a-x1)
    w6 = w4 + (w5-w4)/(y2-y1)*(b-y1)
    w7 = w3 + (w6-w3)/(z2-z1)*(c-z1)
    u = w7
    return u
pos = atoms.get_positions()
P1 = np.array([0.0, 5.0, 5.0])
P2 = np.array([9.0, 5.0, 5.0])
npoints = 60
points = [P1 + n*(P2-P1)/npoints for n in range(npoints)]
R = [np.linalg.norm(p-P1) for p in points]
# interpolated line
icd = [interp3d(x,y,z,cd,p[0],p[1],p[2]) for p in points]
import matplotlib.pyplot as plt
plt.plot(R, icd)
cR = np.linalg.norm(pos[0] - P1)
oR = np.linalg.norm(pos[1] - P1)
plt.plot([cR, cR], [0, 2], 'r-') #markers for where the nuclei are
plt.plot([oR, oR], [0, 8], 'r-')
plt.xlabel('|R| ($\AA$)')
plt.ylabel('Charge density (e/$\AA^3$)')
plt.savefig('images/CO-charge-density.png')
plt.show()