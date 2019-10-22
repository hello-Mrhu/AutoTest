import xlrd

file = '/Users/huchengjiang/Desktop/NewEdition/pn/data/data.xls'
fn = xlrd.open_workbook(file)
print(fn)