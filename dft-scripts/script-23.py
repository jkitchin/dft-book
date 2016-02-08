from jasp import *
L = [4, 5, 6, 8, 10]
for a in L:
    with jasp('molecules/co-L-{0}'.format(a)) as calc:
        print('{0} {1} seconds'.format(a, calc.get_elapsed_time()))