'''
adapted from https://listserv.fysik.dtu.dk/pipermail/campos/2004-September/001155.html
'''
from ase import *
from ase.io import write
from ase.lattice.surface import bcc111, add_adsorbate
from ase.constraints import FixAtoms
# the bcc111 function automatically tags atoms
slab = bcc111('W',
              a=3.92,       # W lattice constant
              size=(2, 2, 6),  # 6-layer slab in 2x2 configuration
              vacuum=10.0)
# reset tags to be powers of two so we can use binary math
slab.set_tags([2**a.get_tag() for a in slab])
# we had 6 layers, so we create new tags starting at 7
# Note you must use powers of two for all the tags!
LAYER1 = 2
ADSORBATE = 2**7
FREE = 2**8
NEARADSORBATE = 2**9
# let us tag LAYER1 atoms to be FREE too. we can address it by LAYER1 or FREE
tags = slab.get_tags()
for i, tag in enumerate(tags):
    if tag == LAYER1:
        tags[i] += FREE
slab.set_tags(tags)
# create a CO molecule
co=Atoms([Atom('C', [0., 0., 0.], tag=ADSORBATE),
          # we will relax only O
          Atom('O', [0., 0., 1.1], tag=ADSORBATE + FREE)])
add_adsorbate(slab, co, height=1.2, position='hollow')
# the adsorbate is centered between atoms 20, 21 and 22 (use
# view(slab)) and over atom12 let us label those atoms, so it is easy to
# do electronic structure analysis on them later.
tags = slab.get_tags()  # len(tags) changed, so we reget them.
tags[12] += NEARADSORBATE
tags[20] += NEARADSORBATE
tags[21] += NEARADSORBATE
tags[22] += NEARADSORBATE
slab.set_tags(tags)
# update the tags
slab.set_tags(tags)
# extract pieces of the slab based on tags
# atoms in the adsorbate
ads = slab[(slab.get_tags() & ADSORBATE) == ADSORBATE]
# atoms in LAYER1
layer1 = slab[(slab.get_tags() & LAYER1) == LAYER1]
# atoms defined as near the adsorbate
nearads = slab[(slab.get_tags() & NEARADSORBATE) == NEARADSORBATE]
# atoms that are free
free = slab[(slab.get_tags() & FREE) == FREE]
# atoms that are FREE and part of the ADSORBATE
freeads = slab[(slab.get_tags() & FREE+ADSORBATE) == FREE+ADSORBATE]
# atoms that are NOT FREE
notfree = slab[(slab.get_tags() & FREE) != FREE]
constraint = FixAtoms(mask=(slab.get_tags() & FREE) != FREE)
slab.set_constraint(constraint)
write('images/tagged-bcc111.png', slab, rotation='-90x', show_unit_cell=2)
from ase.visualize import view; view(slab)