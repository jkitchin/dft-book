from ase.units import *
d = 1 * Angstrom
print(' d = {0} nm'.format(d / nm))
print('1 eV = {0} Hartrees'.format(eV / Hartree))
print('1 eV = {0} Rydbergs'.format(eV / Rydberg))
print('1 eV = {0} kJ/mol'.format(eV / (kJ / mol)))
print('1 eV = {0} kcal/mol'.format(eV / (kcal / mol)))
print('1 Hartree = {0} kcal/mol'.format(1 * Hartree / (kcal / mol)))
print('1 Rydberg = {0} eV'.format(1 * Rydberg / eV))
# derived units
minute = 60 * s
hour = 60 * minute
# convert 10 hours to minutes
print('10 hours = {0} minutes'.format(10 * hour / minute))