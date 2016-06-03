from vasp import Vasp
from ase import Atom, Atoms
calcs = []
for i, a in enumerate([4.7, 5.38936, 6.0]):
    atoms = Atoms([Atom('Si', [0, 0, 0]),
                   Atom('Si', [0.25, 0.25, 0.25])])
    atoms.set_cell([[a/2., a/2., 0.0],
                    [0.0,  a/2., a/2.],
                    [a/2., 0.0, a/2.]], scale_atoms=True)
    calc = Vasp('bulk/Si-bs-{0}'.format(i),
                xc='PBE',
                lcharg=True,
                lwave=True,
                kpts=[4, 4, 4],
                atoms=atoms)
    print(calc.run())
    calcs += [calc]
Vasp.wait(abort=True)
for i, calc in enumerate(calcs):
    n, bands, p  = calc.get_bandstructure(kpts_path=[('L', [0.5,0.5,0.0]),
                                                     ('$\Gamma$', [0, 0, 0]),
                                                     ('$\Gamma$', [0, 0, 0]),
                                                     ('X', [0.5, 0.5, 0.5])],
                                          kpts_nintersections=10)
    if p is not None:
        png = 'images/Si-bs-{0}.png'.format(i)
        p.savefig(png)