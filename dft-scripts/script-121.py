from vasp import Vasp
from ase.lattice.cubic import FaceCenteredCubic
from ase import Atoms, Atom
# bulk system
atoms = FaceCenteredCubic(directions=[[0, 1, 1],
                                      [1, 0, 1],
                                      [1, 1, 0]],
                                      size=(1, 1, 1),
                                      symbol='Rh')
calc = Vasp('bulk/bulk-rh',
            xc='PBE',
            encut=350,
            kpts=[4, 4, 4],
            isif=3,
            ibrion=2,
            nsw=10,
            atoms=atoms)
bulk_energy = atoms.get_potential_energy()
# atomic system
atoms = Atoms([Atom('Rh',[5, 5, 5])],
              cell=(7, 8, 9))
calc = Vasp('bulk/atomic-rh',
            xc='PBE',
            encut=350,
            kpts=[1, 1, 1],
            atoms=atoms)
atomic_energy = atoms.get_potential_energy()
calc.stop_if(None in (bulk_energy, atomic_energy))
cohesive_energy = atomic_energy - bulk_energy
print 'The cohesive energy is {0:1.3f} eV'.format(cohesive_energy)