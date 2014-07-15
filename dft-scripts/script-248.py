nPd = 4
nCu = 5
x_Cu = nCu/(nPd + nCu)
print 'x_cu = {0} (integer division)'.format(x_Cu)
# now cast as floats
x_Cu = float(nCu)/float(nPd + nCu)
print 'x_cu = {0} (float division)'.format(x_Cu)