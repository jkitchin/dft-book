from vasp import Vasp
e_slab_o = Vasp('surfaces/Pt-slab-1x1-O-fcc').potential_energy
# clean slab
e_slab = Vasp('surfaces/Pt-slab-1x1').potential_energy
e_O2 = Vasp('molecules/O2-sp-triplet-350').potential_energy
hads = e_slab_o - e_slab - 0.5 * e_O2
print 'Hads (1ML) = {0:1.3f} eV'.format(hads)