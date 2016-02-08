from jasp import *
from ase.lattice.cubic import BodyCenteredCubic
atoms = BodyCenteredCubic(directions=[[1, 0, 0],
                                      [0, 1, 0],
                                      [0, 0, 1]],
                                      size=(1, 1, 1),
                                      symbol='Fe')
# set magnetic moments on each atom
for atom in atoms:
    atom.magmom = 2.5
with jasp('bulk/Fe-bcc-sp-1',
          xc='PBE',
          encut=300,
          kpts=(4, 4, 4),
          ispin=2,
          lorbit=11, # you need this for individual magnetic moments
          atoms=atoms) as calc:
        try:
            e = atoms.get_potential_energy()
            B = atoms.get_magnetic_moment()
            magmoms = atoms.get_magnetic_moments()
        except (VaspSubmitted, VaspQueued):
            pass
print 'Total magnetic moment is {0:1.2f} Bohr-magnetons'.format(B)
print 'Individual moments are {0} Bohr-magnetons'.format(magmoms)