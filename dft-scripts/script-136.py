# get bulk Cu and Pd energies. <<pure-metal-components>>
from vasp import Vasp
from ase import Atom, Atoms
atoms = Atoms([Atom('Cu',  [0.000,      0.000,      0.000])],
              cell=  [[ 1.818,  0.000,  1.818],
                      [ 1.818,  1.818,  0.000],
                      [ 0.000,  1.818,  1.818]])
cuc = Vasp('bulk/alloy/cu',
          xc='PBE',
          encut=350,
          kpts=[13, 13, 13],
          nbands=9,
          ibrion=2,
          isif=3,
          nsw=10,
          atoms=atoms)
cu = cuc.potential_energy
atoms = Atoms([Atom('Pd',  [0.000,      0.000,      0.000])],
              cell=[[ 1.978,  0.000,  1.978],
                    [ 1.978,  1.978,  0.000],
                    [0.000,  1.978,  1.978]])
pd = Vasp('bulk/alloy/pd',
          xc='PBE',
          encut=350,
          kpts=[13, 13, 13],
          nbands=9,
          ibrion=2,
          isif=3,
          nsw=10,
          atoms=atoms).potential_energy
print 'Cu energy = {0} eV'.format(cu)
print 'Pd energy = {0} eV'.format(pd)