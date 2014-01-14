encuts = [250, 300, 350, 400, 450, 500, 550]
print 'encut (eV)            Total CPU time'
print '--------------------------------------------------------'
for encut in encuts:
    OUTCAR = 'molecules/O2-sp-triplet-{0}/OUTCAR'.format(encut)
    f = open(OUTCAR, 'r')
    for line in f:
        if 'Total CPU time used (sec)' in line:
            print '{0} eV: {1}'.format(encut, line)
    f.close()