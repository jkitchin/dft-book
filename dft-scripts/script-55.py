from vasp import Vasp
# read in relaxed geometry
calc = Vasp('molecules/h2o_relax')
atoms = calc.get_atoms()
# now define a new calculator
calc = Vasp('molecules/h2o_vib_dfpt',
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
            atoms=atoms)
print(calc.potential_energy)