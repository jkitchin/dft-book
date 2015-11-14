from jasp import *
# read in relaxed geometry
with jasp('molecules/h2o_relax') as calc:
    atoms = calc.get_atoms()
# now define a new calculator
with jasp('molecules/h2o_vib_dfpt',
          xc='PBE',
          encut=400,
          ismear=0,  # Gaussian smearing
          ibrion=7,  # switches on the DFPT vibrational analysis (with
                     # no symmetry constraints)
          nfree=2,
          potim=0.015,
          lepsilon=True,  # enables to calculate and to print the BEC
                          # tensors
          lreal=False,
          nsw=1,
          nwrite=3,  # affects OUTCAR verbosity: explicitly forces
                     # SQRT(mass)-divided eigenvectors to be printed
          atoms=atoms) as calc:
    calc.calculate(atoms)