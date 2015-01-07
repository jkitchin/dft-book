from jasp import *
from jasp.jasp_bandstructure import *
from ase import Atom, Atoms
ready = True
for i,a in enumerate([4.7, 5.38936, 6.0]):
    atoms = Atoms([Atom('Si', [0, 0, 0]),
                   Atom('Si', [0.25, 0.25, 0.25])])
    atoms.set_cell([[a/2., a/2., 0.0],
                    [0.0,  a/2., a/2.],
                    [a/2., 0.0, a/2.]], scale_atoms=True)
    with jasp('bulk/Si-bs-{0}'.format(i),
              xc='PBE',
              prec='Medium',
              istart=0,
              icharg=2,
              ediff=0.1e-03,
              kpts=(4, 4, 4),
              atoms=atoms) as calc:
        try:
            n,bands,p  = calc.get_bandstructure(kpts_path=[('L', [0.5,0.5,0.0]),
                                                       ('$\Gamma$', [0, 0, 0]),
                                                       ('$\Gamma$', [0, 0, 0]),
                                                       ('X', [0.5, 0.5, 0.5])],
                                            kpts_nintersections=10)
        except (VaspSubmitted, VaspQueued):
            print 'not ready {0}'.format(i)
            ready = False
    if not ready:
        import sys; sys.exit()
    p.savefig('images/Si-bs-{0}.png'.format(i))
    p.show()