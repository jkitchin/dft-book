from vasp import Vasp
from ase.lattice.surface import fcc111, add_adsorbate
from ase.constraints import FixAtoms, FixScaled
from ase.io import write
atoms = fcc111('Pt', size=(2, 2, 3), vacuum=10.0)
# note this function only works when atoms are created by the surface module.
add_adsorbate(atoms, 'O', height=1.2, position='bridge')
constraint1 = FixAtoms(mask=[atom.symbol != 'O' for atom in atoms])
# fix in xy-direction, free in z. actually, freeze movement in surface
# unit cell, and free along 3rd lattice vector
constraint2 = FixScaled(atoms.get_cell(), 12, [True, True, False])
atoms.set_constraint([constraint1, constraint2])
write('images/Pt-O-bridge-constrained-initial.png', atoms, show_unit_cell=2)
print 'Initial O position: {0}'.format(atoms.positions[-1])
calc = Vasp('surfaces/Pt-slab-O-bridge-xy-constrained',
            xc='PBE',
            kpts=[4, 4, 1],
            encut=350,
            ibrion=2,
            nsw=25,
            atoms=atoms)
e_bridge = atoms.get_potential_energy()
write('images/Pt-O-bridge-constrained-final.png', atoms, show_unit_cell=2)
print 'Final O position  : {0}'.format(atoms.positions[-1])
# now compute Hads
calc = Vasp('surfaces/Pt-slab')
atoms = calc.get_atoms()
e_slab = atoms.get_potential_energy()
calc = Vasp('molecules/O2-sp-triplet-350')
atoms = calc.get_atoms()
e_O2 = atoms.get_potential_energy()
calc.stop_if(None in [e_bridge, e_slab, e_O2])
Hads_bridge = e_bridge - e_slab - 0.5*e_O2
print 'Hads (bridge) = {0:1.3f} eV/O'.format(Hads_bridge)