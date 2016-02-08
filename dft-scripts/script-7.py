from ase.data import g2
keys = g2.data.keys()
# print in 3 columns
for i in range(len(keys) / 3):
    print('{0:25s}{1:25s}{2:25s}'.format(*tuple(keys[i * 3: i * 3 + 3])))