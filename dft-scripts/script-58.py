from vasp import Vasp
calc = Vasp('molecules/h2o_vib_dfpt')
print('mode  Relative intensity')
for i, intensity in enumerate(calc.get_infrared_intensities()):
    print('{0:02d}     {1:1.3f}'.format(i, intensity))