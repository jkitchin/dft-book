from ase.units import GPa
from numpy import array, linspace, polyval
anatase_epars = array([ -1.06049246e-03,   1.30279404e-01,  -5.23520055e+00,
         4.25202869e+01])
rutile_epars = array([ -1.24680208e-03,   1.42966536e-01,  -5.33239733e+00,
         3.85903670e+01])
anatase_ppars = array([  3.18147737e-03,  -2.60558808e-01,   5.23520055e+00])
rutile_ppars = array([  3.74040625e-03,  -2.85933071e-01,   5.33239733e+00])
def func(V):
    V1 = V[0] # rutile volume
    V2 = V[1] # anatase volume
    E_rutile = polyval(rutile_epars,V1)
    E_anatase = polyval(anatase_epars,V2)
    P_rutile =  polyval(rutile_ppars,V1)
    P_anatase = polyval(anatase_ppars,V2)
    return [(E_anatase - E_rutile)/(V1-V2) - P_anatase,
            (E_anatase - E_rutile)/(V1-V2) - P_rutile]
from scipy.optimize import fsolve
x0 = fsolve(func,[28,34])
print 'The solutions are at V = {0}'.format(x0)
print 'Anatase pressure: {0} GPa'.format(polyval(anatase_ppars,x0[1])/GPa)
print 'Rutile  pressure: {0} GPa'.format(polyval(rutile_ppars,x0[0])/GPa)
# illustrate the common tangent
import matplotlib.pyplot as plt
vfit = linspace(28,40)
plt.plot(vfit, polyval(anatase_epars,vfit),label='anatase')
plt.plot(vfit, polyval(rutile_epars,vfit),label='rutile')
plt.plot(x0, [polyval(rutile_epars,x0[0]),
              polyval(anatase_epars,x0[1])], 'ko-', label='common tangent')
plt.legend()
plt.xlabel('Volume ($\AA^3$/f.u.)')
plt.ylabel('Total energy (eV/f.u.)')
plt.savefig('images/eos-common-tangent.png')