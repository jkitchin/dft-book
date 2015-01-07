import multiprocessing
from jasp import *
from ase import Atom, Atoms
from ase.utils.eos import EquationOfState
import numpy as np
# this is the function that runs a calculation
def do_calculation(calculator):
    'function to run a calculation through multiprocessing'
    with calculator as calc:
        atoms = calc.get_atoms()
        e = atoms.get_potential_energy()
        v = atoms.get_volume()
    return v, e
# this only runs in the main script, not in processes on other cores
if __name__ == '__main__':
    NCORES = 6  # number of cores to run processes on
    # setup an atoms object
    a = 3.6
    atoms = Atoms([Atom('Cu',(0, 0, 0))],
                  cell=0.5 * a*np.array([[1.0, 1.0, 0.0],
                                         [0.0, 1.0, 1.0],
                                         [1.0, 0.0, 1.0]]))
    v0 = atoms.get_volume()
    # Step 1
    COUNTER = 0
    calculators = []  # list of calculators to be run
    factors = [-0.1, 0.05, 0.0, 0.05, 0.1]
    for f in factors:
        newatoms = atoms.copy()
        newatoms.set_volume(v0*(1 + f))
        label = 'bulk/cu-mp/step1-{0}'.format(COUNTER)
        COUNTER += 1
        calc = jasp(label,
                    xc='PBE',
                    encut=350,
                    kpts=(6,6,6),
                    isym=2,
                    atoms=newatoms)
        calculators.append(calc)
    # now we set up the Pool of processes
    pool = multiprocessing.Pool(processes=NCORES)
    # get the output from running each calculation
    out = pool.map(do_calculation, calculators)
    pool.close()
    pool.join() # this makes the script wait here until all jobs are done
    # now proceed with analysis
    V = [x[0] for x in out]
    E = [x[1] for x in out]
    eos = EquationOfState(V, E)
    v1, e1, B = eos.fit()
    print 'step1: v1 = {v1}'.format(**locals())
    ### ################################################################
    ## STEP 2, eos around the minimum
    ## #################################################################
    factors = [-0.06, -0.04, -0.02,
               0.0,
               0.02, 0.04, 0.06]
    calculators = [] # reset list
    for f in factors:
        newatoms = atoms.copy()
        newatoms.set_volume(v1*(1 + f))
        label = 'bulk/cu-mp/step2-{0}'.format(COUNTER)
        COUNTER += 1
        calc = jasp(label,
                    xc='PBE',
                    encut=350,
                    kpts=(6,6,6),
                    isym=2,
                    atoms=newatoms)
        calculators.append(calc)
    pool = multiprocessing.Pool(processes=NCORES)
    out = pool.map(do_calculation, calculators)
    pool.close()
    pool.join() # wait here for calculations to finish
    # proceed with analysis
    V += [x[0] for x in out]
    E += [x[1] for x in out]
    V = np.array(V)
    E = np.array(E)
    f = np.array(V)/v1
    # only take points within +- 10% of the minimum
    ind = (f >=0.90) & (f <= 1.1)
    eos = EquationOfState(V[ind], E[ind])
    v2, e2, B = eos.fit()
    print 'step2: v2 = {v2}'.format(**locals())
    eos.plot('images/cu-mp-eos.png')