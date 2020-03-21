from vasp import Vasp
from ase.visualize import view
from ase.lattice.cubic import FaceCenteredCubic
atoms = FaceCenteredCubic(directions=[[0, 1, 1],
                                      [1, 0, 1],
                                      [1, 1, 0]],
                                      size=(1, 1, 1),
                                      symbol='Ag')
Vasp('bulk/Ag-fcc',
     xc='PBE',
     encut=350,
     kpts=[12, 12, 12],
     atoms=atoms).update()