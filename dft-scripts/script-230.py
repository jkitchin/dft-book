from jasp import *
with jasp('molecules/CO-vacuum') as calc:
    calc.clone('molecules/CO-solvated')
with jasp('molecules/CO-solvated',
          istart=1,  #
          lsol=True) as calc:
    print(calc.get_atoms().get_potential_energy())
    print(calc.get_atoms().get_forces())
    print('Calculation time: {} seconds'.format(calc.get_elapsed_time()))