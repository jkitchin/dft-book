from jasp import *
print '**** Calculation summaries'
print '***** CO'
with jasp('molecules/wgs/CO') as calc:
    print '#+begin_example'
    print calc
    print '#+end_example'
print '***** CO2'
with jasp('molecules/wgs/CO2') as calc:
    print '#+begin_example'
    print calc
    print '#+end_example'
print '***** H2'
with jasp('molecules/wgs/H2') as calc:
    print '#+begin_example'
    print calc
    print '#+end_example'
print '***** H2O'
with jasp('molecules/wgs/H2O') as calc:
    print '#+begin_example'
    print calc
    print '#+end_example'