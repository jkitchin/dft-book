#!/usr/bin/env python
from ase import *
from ase.structure import molecule
from jasp import *
import bisect
def vinterp3d(x, y, z, u, xi, yi, zi):
    "Interpolate the point (xi, yi, zi) from the values at u(x, y, z)"
    p = np.array([xi, yi, zi])
    #1D arrays of coordinates
    xv = x[:, 0, 0]
    yv = y[0, :, 0]
    zv = z[0, 0, :]
    # we subtract 1 because bisect tells us where to insert the
    # element to maintain an ordered list, so we want the index to the
    # left of that point
    i = bisect.bisect_right(xv, xi) - 1
    j = bisect.bisect_right(yv, yi) - 1
    k = bisect.bisect_right(zv, zi) - 1
    if i == len(x) - 1:
        i = len(x) - 2
    elif i < 0:
        i = 0
    if j == len(y) - 1:
        j = len(y) - 2
    elif j < 0:
        j = 0
    if k == len(z) - 1:
        k = len(z) - 2
    elif k < 0:
        k = 0
    # points at edge of cell. We only need P1, P2, P3, and P5
    P1 = np.array([x[i, j, k],
                   y[i, j, k],
                   z[i, j, k]])
    P2 = np.array([x[i + 1, j, k],
                   y[i + 1, j, k],
                   z[i + 1, j, k]])
    P3 = np.array([x[i, j + 1, k],
                   y[i, j + 1, k],
                   z[i, j + 1, k]])
    P5 = np.array([x[i, j, k + 1],
                   y[i, j, k + 1],
                   z[i, j, k + 1]])
    # values of u at edge of cell
    u1 = u[i, j, k]
    u2 = u[i+1, j, k]
    u3 = u[i, j+1, k]
    u4 = u[i+1, j+1, k]
    u5 = u[i, j, k+1]
    u6 = u[i+1, j, k+1]
    u7 = u[i, j+1, k+1]
    u8 = u[i+1, j+1, k+1]
    # cell basis vectors, not the unit cell, but the voxel cell containing the point
    cbasis = np.array([P2 - P1,
                       P3 - P1,
                       P5 - P1])
    # now get interpolated point in terms of the cell basis
    s = np.dot(np.linalg.inv(cbasis.T), np.array([xi, yi, zi]) - P1)
    # now s = (sa, sb, sc) which are fractional coordinates in the vector space
    # next we do the interpolations
    ui1 = u1 + s[0] * (u2 - u1)
    ui2 = u3 + s[0] * (u4 - u3)
    ui3 = u5 + s[0] * (u6 - u5)
    ui4 = u7 + s[0] * (u8 - u7)
    ui5 = ui1 + s[1] * (ui2 - ui1)
    ui6 = ui3 + s[1] * (ui4 - ui3)
    ui7 = ui5 + s[2] * (ui6 - ui5)
    return ui7
### Setup calculators
with jasp('molecules/benzene') as calc:
    benzene = calc.get_atoms()
    x1, y1, z1, cd1 = calc.get_charge_density()
with jasp('molecules/chlorobenzene') as calc:
    x2, y2, z2, cd2 = calc.get_charge_density()
cdiff = cd2 - cd1
#we need the x-y plane at z=5
import matplotlib.pyplot as plt
from scipy import mgrid
X, Y = mgrid[0: 10: 25j, 0: 10: 25j]
cdiff_plane = np.zeros(X.shape)
ni, nj = X.shape
for i in range(ni):
    for j in range(nj):
        cdiff_plane[i, j] = vinterp3d(x1, y1, z1, cdiff, X[i, j], Y[i, j], 5.0)
plt.imshow(cdiff_plane,
           vmin=-0.02,  # min charge diff to plot
           vmax=0.02,  # max charge diff to plot
           cmap=plt.cm.gist_heat,  # colormap
           extent=(0., 10., 0., 10.))  # axes limits
# plot atom positions. It is a little tricky to see why we reverse the x and y coordinates. That is because imshow does that.
x = [a.y for a in benzene]
y = [a.x for a in benzene]
plt.plot(x, y, 'bo')
plt.colorbar() #add colorbar
plt.savefig('images/cdiff-imshow.png')
plt.figure()
plt.contourf(X, Y, cdiff_plane)
plt.plot(y, x, 'ko')
plt.axis('equal')
plt.show()