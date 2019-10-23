"""
调用此函数读取相应的支付宝公钥配置文件
:param public:   传入的公钥字符串
:param private: 传入的私钥字符串
:param  appid:   传入appid

"""

import linecache

# res = {}
# file_path1 = './utils/alipay_public_key.txt'
# file_path2 = './utils/app_private_key.txt'
# line_number = 2


# def read_pay_key():
#     def get_line_context(file_path, line_number):
#         return linecache.getline(file_path, line_number).strip()
#
#     pub = get_line_context(file_path1, line_number)
#     prv = get_line_context(file_path2, line_number)
#     with open('./utils/appid.txt', 'r', encoding='utf-8') as fp3:
#         appid = fp3.read()
#         fp3.close()
#     res["pub"] = pub
#     res['prv'] = prv
#     res['appid'] = appid
#     return res

def read_pay_key():
    res = {}
    with open('./utils/alipay_public_key.txt','r',encoding='utf-8') as fp1:
        pub = fp1.readlines()[1]
        fp1.close()
    with open('./utils/app_private_key.txt','r',encoding='utf-8') as fp2:
        prv = fp2.readlines()[1]
        fp2.close()
    with open('./utils/appid.txt', 'r', encoding='utf-8') as fp3:
        appid = fp3.read()
        fp2.close()
    res["pub"] = pub.strip()
    res['prv'] = prv.strip()
    res['appid'] = appid.strip()
    return res
