# 写入excel
import xlwt


def write(data, name):
    wbx = xlwt.Workbook()
    sheet = wbx.add_sheet('Sheet1', cell_overwrite_ok=True)
    for row, i in enumerate(data):
        col = 0
        for j in i:
            sheet.write(row, col, i[j])
            col += 1
    wbx.save(name)