from jasp import *
with jasp('surfaces/Pt-slab-1x1-O-fcc') as calc:
    atoms = calc.get_atoms()
    e_slab_o = atoms.get_potential_energy()
# clean slab
with jasp('surfaces/Pt-slab-1x1') as calc:
    atoms = calc.get_atoms()
    e_slab = atoms.get_potential_energy()
with jasp('molecules/O2-sp-triplet-350') as calc:
    atoms = calc.get_atoms()
    e_O2 = atoms.get_potential_energy()
hads = e_slab_o - e_slab - 0.5*e_O2
print 'Hads (1ML) = {0:1.3f} eV'.format(hads)