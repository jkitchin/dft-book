from vasp import Vasp
calc = Vasp('molecules/CO-vacuum')
calc.clone('molecules/CO-solvated')
calc.set(istart=1,  #
         lsol=True)
print(calc.get_atoms().get_potential_energy())
print(calc.get_atoms().get_forces())
print('Calculation time: {} seconds'.format(calc.get_elapsed_time()))