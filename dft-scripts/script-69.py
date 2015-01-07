from jasp import *
# get relaxed geometry
with jasp('molecules/wgs/CO') as calc:
    CO = calc.get_atoms()
# now do the vibrations
with jasp('molecules/wgs/CO-vib',
          xc='PBE',
          encut=350,
          ismear=0,
          ibrion=6,
          nfree=2,
          potim=0.02,
          nsw=1,
          atoms=CO) as calc:
    calc.calculate()
    vib_freq = calc.get_vibrational_frequencies()
    for i, f in enumerate(vib_freq):
        print '{0:02d}: {1} cm^(-1)'.format(i,f)