import xlrd
wbk = xlrd.open_workbook('images/test-write.xls')
sheet1 = wbk.sheet_by_name('sheet 1')
print sheet1.col_values(0)
print sheet1.col_values(1)