import time
import json
import requests
from website import models


def time_date(subscribe_time):

    # 转换为其他日期格式,如:"%Y-%m-%d %H:%M:%S"
    timeArray = time.localtime(subscribe_time)
    otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    print(otherStyleTime)

    return otherStyleTime

# 获取当前时间
def get_now_tim():
    time_str = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
    return time_str


# 从数据库中获取token函数
def get_acesstoken():
    access_token = models.Token.objects.values('token').first()['token']
    return access_token



# 通过openid 获取用户的基本信息
def get_info(openID):
    token = get_acesstoken()
    url = 'https://api.weixin.qq.com/cgi-bin/user/info'
    parmes = {
        'access_token':token,
        'openid':openID,
        'lang':'zh_CN'
    }
    res = requests.get(url=url,params=parmes).text
    res_dict = json.loads(res)
    print(res_dict)
    return res_dict

# 获取所有用户列表-openID列表
def get_user():
    rest = {'code':0,'data':'','message':''}
    token = get_acesstoken()
    print(token)
    url2 = 'https://api.weixin.qq.com/cgi-bin/user/get'
    parmes = {
        'access_token':token,
        'next_openid':""
    }
    openID_list = []
    count = 0
    total = 0
    while True:
        res = requests.get(url=url2,params=parmes).text
        res_dict = json.loads(res)
        openID_list += res_dict['data']['openid']
        count += res_dict['count']
        total += res_dict['total']
        if res_dict['count'] > 10000:
            parmes['next_openid'] = res_dict['next_openid']
            continue
        else:
            break
    data = {}
    data['count'] = count
    data['total'] = total
    data['openID_list'] = openID_list
    rest['data'] = data
    return rest

