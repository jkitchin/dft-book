from vasp import Vasp
from ase.lattice.cubic import BodyCenteredCubic
atoms = BodyCenteredCubic(directions=[[1, 0, 0],
                                      [0, 1, 0],
                                      [0, 0, 1]],
                                      size=(1, 1, 1),
                                      symbol='Fe')
calc = Vasp('bulk/Fe-bcc-fixedmagmom-{0:1.2f}'.format(0.0),
            xc='PBE',
            encut=300,
            kpts=[4, 4, 4],
            ispin=2,
            nupdown=0,
            atoms=atoms)
print(atoms.get_potential_energy())