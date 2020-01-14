
"""
调用此函数生成相应的支付宝公钥配置文件
:param public:   传入的公钥字符串
:param private: 传入的私钥字符串
:param  appid:   传入appid

"""

def write_pay_key(public,private,appid):
    if type(public) == str and type(private) == str:
        public = public.strip()
        private = private.strip()
        appid = appid.strip()
        # 判断APPID的格式是否是纯数字
        if appid.isdigit():
            pus = '-----BEGIN PUBLIC KEY-----'+'\n' + public + '\n' +'-----END PUBLIC KEY-----'
            prs = '-----BEGIN PUBLIC KEY-----'+'\n' + private + '\n' + '-----END PUBLIC KEY-----'
            with open('./utils/alipay_public_key.txt','w',encoding='utf-8') as fp1:
                fp1.write(pus)
                fp1.close()
            with open('./utils/app_private_key.txt','w',encoding='utf-8') as fp2:
                fp2.write(prs)
                fp2.close()
            if type(appid) == str:
                with open('./utils/appid.txt', 'w', encoding='utf-8') as fp3:
                    fp3.write(appid)
                    fp3.close()
            else:
                return 'appid 写入失败'
            return '写入成功'
        else:
            return 'APPID格式不正确请重新输入！'
    else:
        return '格式不正确，不是字符串'

