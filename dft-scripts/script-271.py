from jasp import *
with jasp('bulk/alloy/cu') as calc:
    print(calc.python)