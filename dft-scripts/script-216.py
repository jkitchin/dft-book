from vasp import Vasp
for U in [2.0, 4.0, 6.0]:
    ## Cu2O ########################################
    calc = Vasp('bulk/Cu2O')
    calc.clone('bulk/Cu2O-U={0}'.format(U))
    calc.set(ldau=True,   # turn DFT+U on
             ldautype=2,  # select simplified rotationally invariant option
             ldau_luj={'Cu':{'L':2,  'U':U, 'J':0.0},
                       'O':{'L':-1, 'U':0.0, 'J':0.0}},
             ldauprint=1,
             ibrion=-1,  # do not rerelax
             nsw=0)
    atoms1 = calc.get_atoms()
    cu2o_energy = atoms1.get_potential_energy() / (len(atoms1) / 3)
    ## CuO ########################################
    calc = Vasp('bulk/CuO')
    calc.clone('bulk/CuO-U={0}'.format(U))
    calc.set(ldau=True,   # turn DFT+U on
             ldautype=2,  # select simplified rotationally invariant option
             ldau_luj={'Cu':{'L':2,  'U':U, 'J':0.0},
                       'O':{'L':-1, 'U':0.0, 'J':0.0}},
             ldauprint=1,
             ibrion=-1,  # do not rerelax
             nsw=0)
    atoms2 = calc.get_atoms()
    cuo_energy = atoms2.get_potential_energy() / (len(atoms2) / 2)
    ## O2 ########################################
    # make sure to use the same cutoff energy for the O2 molecule!
    calc = Vasp('molecules/O2-sp-triplet-400')
    atoms = calc.get_atoms()
    o2_energy = atoms.get_potential_energy()
    if not None in [cu2o_energy, cuo_energy, o2_energy]:
        rxn_energy = (4.0 * cuo_energy
                      - o2_energy
                      - 2.0 * cu2o_energy)
        print 'U = {0}  reaction energy = {1}'.format(U, rxn_energy - 1.99)