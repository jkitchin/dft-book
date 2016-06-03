from ase.structure import molecule
from vasp import Vasp
# first we define our molecules. These will automatically be at the coordinates from the G2 database.
CO = molecule('CO')
CO.set_cell([8, 8, 8], scale_atoms=False)
H2O = molecule('H2O')
H2O.set_cell([8, 8, 8], scale_atoms=False)
CO2 = molecule('CO2')
CO2.set_cell([8, 8, 8], scale_atoms=False)
H2 = molecule('H2')
H2.set_cell([8, 8, 8], scale_atoms=False)
# now the calculators to get the energies
c1 = Vasp('molecules/wgs/CO',
          xc='PBE',
          encut=350,
          ismear=0,
          ibrion=2,
          nsw=10,
          atoms=CO)
eCO = CO.get_potential_energy()
c2 = Vasp('molecules/wgs/CO2',
          xc='PBE',
          encut=350,
          ismear=0,
          ibrion=2,
          nsw=10,
          atoms=CO2)
eCO2 = CO2.get_potential_energy()
c3 = Vasp('molecules/wgs/H2',
          xc='PBE',
          encut=350,
          ismear=0,
          ibrion=2,
          nsw=10,
          atoms=H2)
eH2 = H2.get_potential_energy()
c4 = Vasp('molecules/wgs/H2O',
          xc='PBE',
          encut=350,
          ismear=0,
          ibrion=2,
          nsw=10,
          atoms=H2O)
eH2O = H2O.get_potential_energy()
if None in (eCO2, eH2, eCO, eH2O):
    pass
else:
    dE = eCO2 + eH2 - eCO - eH2O
    print('Delta E = {0:1.3f} eV'.format(dE))
    print('Delta E = {0:1.3f} kcal/mol'.format(dE * 23.06035))
    print('Delta E = {0:1.3f} kJ/mol'.format(dE * 96.485))