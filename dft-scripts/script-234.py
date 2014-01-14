#!/usr/bin/env python
import os
serial_vasp = '/home/jkitchin/src/vasp/bin/vasp_serial_intel_mkl'
parallel_vasp = '/home/jkitchin/src/vasp/bin/vasp_openmpi_intel_mkl'
if 'PBS_NODEFILE' in os.environ:
    NPROCS = len(open(os.environ['PBS_NODEFILE']).readlines())
    if NPROCS == 1:
        print 'NPROCS = ',NPROCS
        exitcode = os.system(serial_vasp)
    else:
        print 'NPROCS = ',NPROCS
        parcmd = 'mpirun -np %i %s' % (NPROCS,parallel_vasp)
        exitcode = os.system(parcmd)
else:
    exitcode = os.system(serial_vasp)
#end