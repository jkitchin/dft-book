v1 = []
v2 = []
lines = open('somefile','r').readlines()
for line in lines[2:]: #skip the first two lines
    fields = line.split(',')
        v1.append(fields[0]) #names
        v2.append(int(fields[1])) #number