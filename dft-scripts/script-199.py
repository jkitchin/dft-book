from jasp import *
for U in [2.0, 4.0, 6.0]:
    ## Cu2O ########################################
    with jasp('bulk/Cu2O') as calc:
        calc.clone('bulk/Cu2O-U={0}'.format(U))
    with jasp('bulk/Cu2O-U={0}'.format(U)) as calc:
        calc.set(ldau=True,   # turn DFT+U on
                 ldautype=2,  # select simplified rotationally invariant option
                 ldau_luj={'Cu':{'L':2,  'U':U, 'J':0.0},
                           'O':{'L':-1, 'U':0.0, 'J':0.0}},
                ldauprint=1,
                ibrion=-1,  #do not rerelax
                nsw=0)
        atoms = calc.get_atoms()
        cu2o_energy = atoms.get_potential_energy()/(len(atoms)/3)
    ## CuO ########################################
    with jasp('bulk/CuO') as calc:
        calc.clone('bulk/CuO-U={0}'.format(U))
    with jasp('bulk/CuO-U={0}'.format(U)) as calc:
        calc.set(ldau=True,   # turn DFT+U on
                 ldautype=2,  # select simplified rotationally invariant option
                 ldau_luj={'Cu':{'L':2,  'U':U, 'J':0.0},
                           'O':{'L':-1, 'U':0.0, 'J':0.0}},
                ldauprint=1,
                ibrion=-1,  #do not rerelax
                nsw=0)
        atoms = calc.get_atoms()
        cuo_energy = atoms.get_potential_energy()/(len(atoms)/2)
    ## O2 ########################################
    # make sure to use the same cutoff energy for the O2 molecule!
    with jasp('molecules/O2-sp-triplet-400') as calc:
        atoms = calc.get_atoms()
        o2_energy = atoms.get_potential_energy()
    rxn_energy = 4.0*cuo_energy - o2_energy - 2.0*cu2o_energy
    print 'U = {0}  reaction energy = {1}'.format(U,rxn_energy - 1.99)