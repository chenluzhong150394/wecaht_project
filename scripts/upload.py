import os


import json

def upload_img():
    file_path = '/img/'
    file_name = os.listdir(file_path)
    ACCESTOEK = '28_gqR3en8INCaLnRS-4lKX4fGTfB720JM2P04AQrz3D4tw_0z2s7pGfKpLUi8UbqTueGndOD4QC00FFmTHZBWSyvCzxEJ4b-2--3ov3Y4_fMBMY0XkOoCLLWYyyaPGXImBtQDr5B7KHbzvBdT_EKCbACATZR'
    METTID = list()
    for i in file_name:
        path = file_path + i
        shell  = 'curl -F media=@' + path + ' '  +  '"https://api.weixin.qq.com/cgi-bin/material/add_material?access_token=' + ACCESTOEK +  '&type=image"'
        #print(shell)
        res = os.popen(shell).readlines() 
        print(type(res))
        res = str(res)
        print(res)
        print(res[15:58])
        #result = json.loads(res)
        #print(result['media_id'])
        METTID.append(res[15:58])
    print(METTID)
    print(file_name)

upload_img()
