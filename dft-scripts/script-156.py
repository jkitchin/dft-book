from vasp import Vasp
calc = Vasp('bulk/tio2/step3')
print calc.get_fermi_level()
calc.abort()
n, bands, p = calc.get_bandstructure(kpts_path=[('$\Gamma$', [0.0, 0.0, 0.0]),
                                                ('X', [0.5, 0.5, 0.0]),
                                                ('X', [0.5, 0.5, 0.0]),
                                                ('M', [0.0, 0.5, 0.5]),
                                                ('M', [0.0, 0.5, 0.5]),
                                                ('$\Gamma$', [0.0, 0.0, 0.0])])
p.savefig('images/tio2-bandstructure-dos.png')