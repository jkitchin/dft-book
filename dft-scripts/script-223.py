import numpy as np
import matplotlib.pyplot as plt
import time
'''
These are the brainless way to calculate numerical derivatives. They
work well for very smooth data. they are surprisingly fast even up to
10000 points in the vector.
'''
x = np.linspace(0.78, 0.79, 100) # 100 points between 0.78 and 0.79
y = np.sin(x)
dy_analytical = np.cos(x)
'''
let us use a forward difference method:
that works up until the last point, where there is not
a forward difference to use. there, we use a backward difference.
'''
tf1 = time.time()
dyf = [0.0]*len(x)
for i in range(len(y)-1):
    dyf[i] = (y[i+1] - y[i])/(x[i+1]-x[i])
#set last element by backwards difference
dyf[-1] = (y[-1] - y[-2])/(x[-1] - x[-2])
print ' Forward difference took {0:1.1f} seconds'.format(time.time() - tf1)
'''and now a backwards difference'''
tb1 = time.time()
dyb = [0.0]*len(x)
#set first element by forward difference
dyb[0] = (y[0] - y[1])/(x[0] - x[1])
for i in range(1,len(y)):
    dyb[i] = (y[i] - y[i-1])/(x[i]-x[i-1])
print ' Backward difference took {0:1.1f} seconds'.format(time.time() - tb1)
'''and now, a centered formula'''
tc1 = time.time()
dyc = [0.0]*len(x)
dyc[0] = (y[0] - y[1])/(x[0] - x[1])
for i in range(1,len(y)-1):
    dyc[i] = (y[i+1] - y[i-1])/(x[i+1]-x[i-1])
dyc[-1] = (y[-1] - y[-2])/(x[-1] - x[-2])
print ' Centered difference took {0:1.1f} seconds'.format(time.time() - tc1)
'''
the centered formula is the most accurate formula here
'''
plt.plot(x,dy_analytical,label='analytical derivative')
plt.plot(x,dyf,'--',label='forward')
plt.plot(x,dyb,'--',label='backward')
plt.plot(x,dyc,'--',label='centered')
plt.legend(loc='lower left')
plt.savefig('images/simple-diffs.png')