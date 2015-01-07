from jasp import *
with jasp('bulk/Ru2O4',
          xc='PBE',
          setups={'Ru': '_pv'}) as calc:
    calc.calculate()
    print calc