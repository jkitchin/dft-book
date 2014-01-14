'''
3D vector interpolation in non-cubic unit cells with vector
interpolation.
This function should work for any shape unit cell.
'''
from jasp import *
import bisect
import numpy as np
from pylab import plot, xlabel, ylabel, savefig, show
with jasp('molecules/co-centered') as calc:
    atoms = calc.get_atoms()
    x,y,z,cd = calc.get_charge_density()
def vinterp3d(x,y,z,u,xi,yi,zi):
    p = np.array([xi,yi,zi])
    #1D arrays of cooridinates
    xv = x[:,0,0]
    yv = y[0,:,0]
    zv = z[0,0,:]
    # we subtract 1 because bisect tells us where to insert the
    # element to maintain an ordered list, so we want the index to the
    # left of that point
    i = bisect.bisect_right(xv,xi) - 1
    j = bisect.bisect_right(yv,yi) - 1
    k = bisect.bisect_right(zv,zi) - 1
    #points at edge of cell. We only need P1, P2, P3, and P5
    P1 = np.array([x[i,j,k],y[i,j,k],z[i,j,k]])
    P2 = np.array([x[i+1,j,k],y[i+1,j,k],z[i+1,j,k]])
    P3 = np.array([x[i,j+1,k],y[i,j+1,k],z[i,j+1,k]])
    P5 = np.array([x[i,j,k+1],y[i,j,k+1],z[i,j,k+1]])
    #values of u at edge of cell
    u1 = u[i,j,k]
    u2 = u[i+1,j,k]
    u3 = u[i,j+1,k]
    u4 = u[i+1,j+1,k]
    u5 = u[i,j,k+1]
    u6 = u[i+1,j,k+1]
    u7 = u[i,j+1,k+1]
    u8 = u[i+1,j+1,k+1]
    #cell basis vectors, not the unit cell, but the voxel cell containing the point
    cbasis = np.array([P2-P1,
                       P3-P1,
                       P5-P1])
    #now get interpolated point in terms of the cell basis
    s = np.dot(np.linalg.inv(cbasis.T),np.array([xi,yi,zi])-P1)
    #now s = (sa, sb, sc) which are fractional coordinates in the vector space
    #next we do the interpolations
    ui1 = u1 + s[0]*(u2-u1)
    ui2 = u3 + s[0]*(u4-u3)
    ui3 = u5 + s[0]*(u6-u5)
    ui4 = u7 + s[0]*(u8-u7)
    ui5 = ui1 + s[1]*(ui2-ui1)
    ui6 = ui3 + s[1]*(ui4-ui3)
    ui7 = ui5 + s[2]*(ui6-ui5)
    return ui7
# compute a line with 60 points in it through these two points
P1 = np.array([0.0, 5.0, 5.0])
P2 = np.array([10.0, 5.0, 5.0])
npoints = 60
points = [P1 + n*(P2-P1)/npoints for n in range(npoints)]
# compute the distance along the line
R = [np.linalg.norm(p-P1) for p in points]
icd = [vinterp3d(x,y,z,cd,p[0],p[1],p[2]) for p in points]
plot(R,icd)
pos = atoms.get_positions()
cR = np.linalg.norm(pos[0]-P1)
oR = np.linalg.norm(pos[1]-P1)
plot([cR,cR],[0,2],'r-') #markers for where the nuclei are
plot([oR,oR],[0,8],'r-')
xlabel('|R| ($\AA$)')
ylabel('Charge density (e/$\AA^3$)')
savefig('images/interpolated-charge-density.png')
show()