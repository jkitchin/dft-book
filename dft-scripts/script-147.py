from jasp import *
from jasp.jasp_bandstructure import *
with jasp('bulk/tio2/step3') as calc:
    n, bands, p = calc.get_bandstructure(kpts_path=[('$\Gamma$', [0.0, 0.0, 0.0]),
                                                  ('X', [0.5, 0.5, 0.0]),
                                                  ('X', [0.5, 0.5, 0.0]),
                                                  ('M', [0.0, 0.5, 0.5]),
                                                  ('M', [0.0, 0.5, 0.5]),
                                                  ('$\Gamma$', [0.0, 0.0, 0.0])])
p.savefig('images/tio2-bandstructure-dos.png')