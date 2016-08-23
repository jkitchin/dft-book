import numpy as np
import matplotlib as mpl
# http://matplotlib.sourceforge.net/users/customizing.html
mpl.rcParams['legend.numpoints'] = 1  # default is 2
import matplotlib.pyplot as plt
x = np.linspace(0, 6, 100)
y = np.cos(x)
plt.plot(x, y, label='full')
ind = (x > 2) & (x < 4)
subx = x[ind]
suby = y[ind]
plt.plot(subx, suby, 'bo', label='sliced')
xlabel('x')
ylabel('cos(x)')
plt.legend(loc='lower right')
plt.savefig('images/np-array-slice.png')