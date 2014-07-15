# use splines to fit and interpolate data
from scipy.interpolate import interp1d
from scipy.optimize import fmin
import numpy as np
import matplotlib.pyplot as plt
x = np.array([ 0,      1,      2,      3,      4    ])
y = np.array([ 0.,     0.308,  0.55,   0.546,  0.44 ])
# create the interpolating function
f = interp1d(x, y, kind='cubic', bounds_error=False)
# to find the maximum, we minimize the negative of the function. We
# cannot just multiply f by -1, so we create a new function here.
f2 = interp1d(x, -y, kind='cubic')
xmax = fmin(f2, 2.5)
xfit = np.linspace(0,4)
plt.plot(x,y,'bo')
plt.plot(xfit, f(xfit),'r-')
plt.plot(xmax, f(xmax),'g*')
plt.legend(['data','fit','max'], loc='best', numpoints=1)
plt.xlabel('x data')
plt.ylabel('y data')
plt.title('Max point = ({0:1.2f}, {1:1.2f})'.format(float(xmax),
                                                    float(f(xmax))))
plt.savefig('images/splinefit.png')