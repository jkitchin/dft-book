from vasp import Vasp
L = [4, 5, 6, 8, 10]
for a in L:
    calc = Vasp('molecules/co-L-{0}'.format(a))
    print('{0} {1} seconds'.format(a, calc.get_elapsed_time()))