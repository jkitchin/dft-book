x0 = 0.0; x3 = 0.5; x = 0.25;
Hf1 = 0.0; Hf3 = -0.12;
print 'Composition weighted average  = {0} eV'.format(Hf1 + (x0-x)/(x0-x3)*(Hf3 - Hf1))