from vasp import Vasp
wd = 'bulk/Si-bandstructure'
calc = Vasp('bulk/Si-selfconsistent')
calc.clone(wd)
kpts = [[0.5, 0.5, 0.0],   # L
        [0, 0, 0],         # Gamma
        [0, 0, 0],
        [0.5, 0.5, 0.5]]  # X
calc.set(kpts=kpts,
         reciprocal=True,
         kpts_nintersections=10,
         icharg=11)
print calc.run()