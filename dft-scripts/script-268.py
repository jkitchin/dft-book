#!/usr/bin/env python
import multiprocessing
from jasp import *
from ase import Atom, Atoms
from ase.utils.eos import EquationOfState
import numpy as np
JASPRC['queue.nodes'] = 1
# Here we will be able to run three MPI jobs on 2 cores at a time.
JASPRC['queue.ppn'] = 6
JASPRC['multiprocessing.cores_per_process'] = 2
# to submit this script, save it as cu-mp.py
# qsub -l nodes=1:ppn=6,walltime=10:00:00 cu-mp.py
import os
if 'PBS_O_WORKDIR' in os.environ:
    os.chdir(os.environ['PBS_O_WORKDIR'])
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
        label = 'bulk/cu-mp2/step1-{0}'.format(COUNTER)
        COUNTER += 1
        calc = jasp(label,
                    xc='PBE',
                    encut=350,
                    kpts=(6,6,6),
                    isym=2,
                    debug=logging.DEBUG,
                    atoms=newatoms)
        calculators.append(calc)
    # now we set up the Pool of processes
    pool = multiprocessing.Pool(processes=3) # ask for 6 cores but run MPI on 2 cores
    # get the output from running each calculation
    out = pool.map(do_calculation, calculators)
    pool.close()
    pool.join() # this makes the script wait here until all jobs are done
    # now proceed with analysis
    V = [x[0] for x in out]
    E = [x[1] for x in out]
    eos = EquationOfState(V, E)
    v1, e1, B = eos.fit()
    print('step1: v1 = {v1}'.format(**locals()))
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
        label = 'bulk/cu-mp2/step2-{0}'.format(COUNTER)
        COUNTER += 1
        calc = jasp(label,
                    xc='PBE',
                    encut=350,
                    kpts=(6,6,6),
                    isym=2,
                    debug=logging.DEBUG,
                    atoms=newatoms)
        calculators.append(calc)
    pool = multiprocessing.Pool(processes=3)
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
    print('step2: v2 = {v2}'.format(**locals()))
    eos.plot('images/cu-mp2-eos.png',show=True)