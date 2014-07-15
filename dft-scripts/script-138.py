from jasp import *
wd = 'bulk/Si-bandstructure'
with jasp('bulk/Si-selfconsistent') as calc:
    calc.clone(wd)
kpts = [[0.5,0.5,0.0],   # L
        [0,0,0],         # Gamma
        [0,0,0],
        [0.5, 0.5, 0.5]] # X
with jasp(wd,
          kpts=kpts,
          reciprocal=True,
          kpts_nintersections=10,
          icharg=11) as calc:
    calc.calculate()