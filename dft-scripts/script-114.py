import numpy as np
EM = []
with open('bulk/Fe-elastic/OUTCAR') as f:
    lines = f.readlines()
    for i, line in enumerate(lines):
        if line.startswith(' TOTAL ELASTIC MODULI (kBar)'):
            j = i + 3
            data = lines[j:j+6]
            break
for line in data:
    EM += [[float(x) for x in line.split()[1:]]]
print np.array(EM)