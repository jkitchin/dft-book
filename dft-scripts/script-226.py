from jasp import *
from ase.dft.bee import BEEFEnsemble
with jasp('molecules/H-beef') as calc:
    BE1 = BEEFEnsemble(calc.get_atoms()).get_ensemble_energies()
with jasp('molecules/H2-beef') as calc:
    BE2 = BEEFEnsemble(calc.get_atoms()).get_ensemble_energies()
print((2 * BE1 - BE2).mean())
print((2 * BE1 - BE2).std())