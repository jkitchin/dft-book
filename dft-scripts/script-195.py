from jasp import *
from ase.lattice.surface import fcc111
atoms = fcc111('Pt', size=(2, 2, 4), vacuum=10.0, a=3.986)
atoms.append(Atom('C', [atoms[12].x, atoms[12].y, atoms[12].z + 1.851]))
atoms.append(Atom('O', [atoms[-1].x, atoms[-1].y, atoms[-1].z + 1.157]))
for field in [-0.5, 0.0, 0.5]:
    with jasp('surfaces/Pt-co-field-{0}'.format(field),
              xc='PBE',
              encut=350,
              kpts=(6, 6, 1),
              efield=field,  # set the field
              ldipol=True,   # turn dipole correction on
              idipol=3,      # set field in z-direction
              atoms=atoms) as calc:
        try:
            print '{0}: {1:1.3f}'.format(field, atoms.get_potential_energy())
        except (VaspSubmitted, VaspQueued):
            pass