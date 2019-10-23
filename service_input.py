# 读取Excel文件

import xlrd

def excel(path):
    try:
        ExcelFile = xlrd.open_workbook(path)
    except Exception as e:
        return

    data = ExcelFile.sheet_by_name(ExcelFile.sheet_names()[0])
    title = data.row_values(0)
    for i in range(len(title)):
        if title[i].startswith('2'):
            if len(title[i]) == 8:
                title[i] = title[i].replace('.', '-0')
            else:
                title[i] = title[i].replace('.', '-')
                title[i] = title[i][0:5] +'0' +title[i][5:]

    re = {}
    buff = {}
    for i in range(1, (data.nrows-1)):
        for index, j in enumerate(data.row_values(i)[2:]):
            if j == '总数':
                break
            if j!= ' ' and j!='':
                buff[title[index+2]] = int(j)
            else:
                buff[title[index + 2]] = 0

        if buff:
            re[data.row_values(i)[0]] = buff
        buff = {}
    return re

# f = read_excel('../files/2018.7.30.xls')

# r = excel('nums.xlsx')
# print(len(r))
# print(r)

# def put(request):
#     if request.method == 'GET':
#         data = excel('nums.xlsx')
#         for i in data:
#             for j in data[i]:
#                 print(i,j,data[i][j])
#                 models.WebsiteInputdata.objects.create(username=i, time=j, data=data[i][j])
#         # print(data)
#         return HttpResponse("OK")