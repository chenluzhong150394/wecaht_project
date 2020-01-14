

import json
import requests
from website import models


# 从数据库中获取token函数
def get_acesstoken():
    access_token = models.Token.objects.values('token').first()['token']
    return access_token



# 通过openid 获取用户的基本信息
def get_info(openID):
    token = get_acesstoken()
    url = 'https://api.weixin.qq.com/cgi-bin/user/info?=ACCESS_TOKEN&=OPENID&='
    parmes = {
        'access_token':token,
        'openid':openID,
        'lang':'zh_CN'
    }
    res = requests.get(url=url,params=parmes).text
    res_dict = json.loads(res)
    print(res_dict)
    return res_dict

