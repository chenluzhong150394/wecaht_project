# 读取Excel文件

import xlrd


def read_excel(path):
    try:
        excel_file = xlrd.open_workbook(path)
    except Exception as e:
        print(e)
        return
    # sheet xls表中sheet的名字
    sheet = excel_file.sheet_names()[0]
    # data xls表中的数据
    data = excel_file.sheet_by_name(sheet)
    #标题行 所以i=1
    i = 1
    while i < data.nrows:
        yield data.row_values(i)
        i += 1












# 测试
# f = read_excel('../files/2018.7.30.xls')
# f = read_excel('a.xls')
# for i in f:
#     print(i)
