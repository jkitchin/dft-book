import csv
reader = csv.reader(open("some.csv",'r'),delimiter=',')
x,y = [],[]
for row in reader:
#csv returns strings that must be cast as floats
    a,b = [float(z) for z in row]
    x.append(a)
    y.append(b)