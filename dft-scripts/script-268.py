import numpy as np
import xlwt
wbk = xlwt.Workbook()
sheet = wbk.add_sheet('sheet 1')
volumes = np.array([13.72, 14.83, 16.0, 17.23, 18.52])
energies = np.array([-56.29, -56.41, -56.46, -56.46, -56.42])
for i, pair in enumerate(zip(volumes, energies)):
    vol = pair[0]
    energy = pair[1]
    sheet.write(i,0,vol)
    sheet.write(i,1,energy)
wbk.save('images/test-write.xls')