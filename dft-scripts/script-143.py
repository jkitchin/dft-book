# run Cu2O calculation
from vasp import Vasp
from ase import Atom, Atoms
# http://phycomp.technion.ac.il/~ira/types.html#Cu2O
a = 4.27
atoms = Atoms([Atom('Cu', [0, 0, 0]),
               Atom('Cu', [0.5, 0.5, 0.0]),
               Atom('Cu', [0.5, 0.0, 0.5]),
               Atom('Cu', [0.0, 0.5, 0.5]),
               Atom('O', [0.25, 0.25, 0.25]),
               Atom('O', [0.75, 0.75, 0.75])])
atoms.set_cell((a, a, a), scale_atoms=True)
calc = Vasp('bulk/Cu2O',
            encut=400,
            kpts=[8, 8, 8],
            ibrion=2,
            isif=3,
            nsw=30,
            xc='PBE',
            atoms=atoms)
print atoms.get_potential_energy()
print atoms.get_stress()