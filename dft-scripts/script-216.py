v1 = ['john', 'robert', 'terry']
v2 = [4,5,6]
f = open('somefile', 'w') #note 'w' = write mode
f.write('#header\n')
f.write('#ignore these lines\n')
for a,b in zip(v1,v2):
        f.write('{0}, {1}\n'.format(a,b))
f.close()