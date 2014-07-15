#examples of linear curve fitting using least squares
import numpy as np
xdata = np.array([0.,1.,2.,3.,4.,5.,6.])
ydata = np.array([0.1, 0.81, 4.03, 9.1, 15.99, 24.2, 37.2])
#fit a third order polynomial
from pylab import polyfit, plot, xlabel, ylabel, show, legend, savefig
pars = polyfit(xdata,ydata,3)
print 'pars from polyfit: {0}'.format(pars)
## numpy method returns more data
A = np.column_stack([xdata**3,
                     xdata**2,
                     xdata,
                     np.ones(len(xdata),np.float)])
pars_np,resids,rank,s = np.linalg.lstsq(A, ydata)
print 'pars from np.linalg.lstsq: {0}'.format(pars_np)
'''
we are trying to solve Ax = b for x in the least squares sense. There
are more rows in A than elements in x so, we can left multiply each
side by A^T, and then solve for x with an inverse.
A^TAx = A^Tb
x = (A^TA)^-1 A^T b
'''
# not as pretty but equivalent!
pars_man= np.dot(np.linalg.inv(np.dot(A.T,A)), np.dot(A.T,ydata))
print 'pars from linear algebra: {0}'.format(pars_man)
#but, it is easy to fit an exponential function to it!
# y = a*exp(x)+b
Aexp = np.column_stack([np.exp(xdata), np.ones(len(xdata), np.float)])
pars_exp=np.dot(np.linalg.inv(np.dot(Aexp.T, Aexp)), np.dot(Aexp.T, ydata))
plot(xdata, ydata, 'ro')
fity = np.dot(A, pars)
plot(xdata, fity, 'k-', label='poly fit')
plot(xdata, np.dot(Aexp, pars_exp), 'b-', label='exp fit')
xlabel('x')
ylabel('y')
legend()
savefig('images/curve-fit-1.png')