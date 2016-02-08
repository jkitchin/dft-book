# get bulk Cu and Pd energies. <<pure-metal-components>>
from jasp import *
from ase import Atom, Atoms
atoms = Atoms([Atom('Cu',  [0.000,      0.000,      0.000])],
              cell=  [[ 1.818,  0.000,  1.818],
                      [ 1.818,  1.818,  0.000],
                      [ 0.000,  1.818,  1.818]])
with jasp('bulk/alloy/cu',
          xc='PBE',
          encut=350,
          kpts=(13, 13, 13),
          nbands=9,
          ibrion=2,
          isif=3,
          nsw=10,
          atoms=atoms) as calc:
    cu = atoms.get_potential_energy()
atoms = Atoms([Atom('Pd',  [0.000,      0.000,      0.000])],
              cell=[[ 1.978,  0.000,  1.978],
                    [ 1.978,  1.978,  0.000],
                    [0.000,  1.978,  1.978]])
with jasp('bulk/alloy/pd',
          xc='PBE',
          encut=350,
          kpts=(13, 13, 13),
          nbands=9,
          ibrion=2,
          isif=3,
          nsw=10,
          atoms=atoms) as calc:
    pd = atoms.get_potential_energy()
print 'Cu energy = {0} eV'.format(cu)
print 'Pd energy = {0} eV'.format(pd)