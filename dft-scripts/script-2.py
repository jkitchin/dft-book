CWD = os.getcwd()
os.chdir('directory')
calc=Vasp(lotsofkeywords)
atoms.set_calculator(calc)
try:
    #do stuff
finally:
    os.chdir(CWD)