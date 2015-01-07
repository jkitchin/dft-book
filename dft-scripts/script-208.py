import numpy as np
from scipy.stats.distributions import  t
n = 10 #number of measurements
dof = n - 1 #degrees of freedom
avg_x = 16.1 #average measurement
std_x = 0.01 #standard deviation of measurements
#Find 95% prediction interval for next measurement
alpha = 1.0 - 0.95
pred_interval = t.ppf(1-alpha/2., dof) * std_x * np.sqrt(1.+1./n)
s = ['We are 95% confident the next measurement',
       ' will be between {0:1.3f} and {1:1.3f}']
print ''.join(s).format(avg_x - pred_interval, avg_x + pred_interval)