from jasp.POTCAR import *
from ase.data import chemical_symbols
import glob, os
print '#+tblname: POTCAR'
print '#+caption: Parameters for POTPAW_PBE POTCAR files.'
print '#+ATTR_LaTeX: longtable'
print '| POTCAR | ENMIN | ENMAX | prec=high (eV) | # val. elect. |'
print '|-'
chemical_symbols.sort()
for symbol in chemical_symbols:
    potcars = glob.glob('{0}/POTPAW_PBE/{1}*/POTCAR'.format(os.environ['VASP_PP_PATH'],
                                                     symbol))
    for potcar in potcars:
        POTCAR = os.path.relpath(potcar,
                                 os.environ['VASP_PP_PATH']+'/POTPAW_PBE')[:-7]
        ENMIN = get_ENMIN(potcar)
        ENMAX = get_ENMAX(potcar)
        HIGH  = 1.3*ENMAX
        ZVAL  = get_ZVAL(potcar)
        print '|{POTCAR:30s}|{ENMIN}|{ENMAX}|{HIGH:1.3f}|{ZVAL}|'.format(**locals())