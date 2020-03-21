from vasp import Vasp
print('**** Calculation summaries')
print('***** CO')
calc = Vasp('molecules/wgs/H2O')
print('#+begin_example')
print(calc)
print('#+end_example')