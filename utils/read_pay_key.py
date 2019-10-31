"""
调用此函数读取相应的支付宝公钥配置文件
:param public:   传入的公钥字符串
:param private: 传入的私钥字符串
:param  appid:   传入appid

"""

def read_pay_key():
    res = {'code': 0, 'message': "", 'data': []}
    with open('./utils/alipay_public_key.txt', 'r', encoding='utf-8') as fp1:
        pub = fp1.readlines()[1]
        fp1.close()
    with open('./utils/app_private_key.txt', 'r', encoding='utf-8') as fp2:
        prv = fp2.readlines()[1]
        fp2.close()
    with open('./utils/appid.txt', 'r', encoding='utf-8') as fp3:
        appid = fp3.read()
        fp2.close()
    res["data"].append({"pub": pub, "prv": prv, "appid": appid})
    return res
