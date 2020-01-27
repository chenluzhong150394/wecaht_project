import os
from django.shortcuts import render, HttpResponse, redirect
from django.http import FileResponse, JsonResponse
# from django.views import View
from website import models
from OA import settings
from .utils1 import create_mch_billno
from website.datebase import *
from rest_framework.views import APIView
import json
from django.db.models import Q
import hashlib
import requests
from xml.etree import ElementTree
from utils.weixinSDK import *

list1 = ['TQUI51nP3YR5J8OZdMCSivqRI5igK15NGvdjUXsODSo', 'TQUI51nP3YR5J8OZdMCSil7bMwLskOLvFP9l4YQLHQ4', 'TQUI51nP3YR5J8OZdMCSijzTkEopkPy_c_uEHNMHR1c', 'TQUI51nP3YR5J8OZdMCSisZ2EA89vq39S7GOaPhj4XI', 'TQUI51nP3YR5J8OZdMCSiqve8pwMeQeMobHhyFro_yc', 'TQUI51nP3YR5J8OZdMCSitAfyaZGWG4NsN2P9ZnL5y4', 'TQUI51nP3YR5J8OZdMCSihKLumbIZZY85ywyDFhgocs', 'TQUI51nP3YR5J8OZdMCSinIrrKVygYMb8ppWP-cQSmQ', 'TQUI51nP3YR5J8OZdMCSil9A9FdaL_Svb8fo6pVa7ck', 'TQUI51nP3YR5J8OZdMCSit5UQtdF3E44lIOxkzk3tt8', 'TQUI51nP3YR5J8OZdMCSivnnQmlIIdjgGt-9XbBrNk0', 'TQUI51nP3YR5J8OZdMCSikJ-2vDdXdwde_RT-Bfpjxw']




# 测试
def test(request):
    print(get_info('o3L5YuPtvki2sjXFsqZpek_uLzi8'))

    # get_user

    return HttpResponse('123')


def regester_user(request):
    body = json.loads(request.body.decode())
    username = body['username']
    password = body['password']
    role = body['role']
    return HttpResponse('sad')


# 获取所有用户的数据
def get_data(request):
    rec = {'code':0,'data':'','msg':''}
    all_data = models.user_openID.objects.all()

    data_str = models.model_to_dict(all_data)

    print('这个是data')
    print(data_str)





# 获取所有的关注者openID 并更新存入数据库中
def get_all_user(request):
    # 初始化返回对象字典
    rec = {'code': 0, 'msg':'','data':''}
    try:
        count_num = 0
        res = get_user()
        openID_list = res['data']['openID_list']
        now_time = get_now_tim()
        for i in openID_list:
            if not models.user_openID.objects.filter(openID=i).first():
                # 不存在则创建
                count_num += 1
                models.user_openID.objects.create(openID=i,create_time=now_time)
                print('增加一条openiD')
        # 开始将所有的openID 更新一遍
        for p in openID_list:
            res = get_info(p)
            sub_time = time_date(res['subscribe_time'])
            query_obj = models.user_openID.objects.filter(openID=p).update(user=res['nickname'],city=res['city'],
                                                                           position=res['country'],headimgurl=res['headimgurl'],
                                                                           subscribe=res['subscribe'],subscribe_time=sub_time,
                                                                           remark=res['remark'])

        # 将新增条数计算出来
        data = {'count_num':count_num}
        rec['data'] = data
    except Exception as e:
        rec = {'code':1,'msg':e.__repr__()}

    return JsonResponse(rec)

#登陆校验（明文账号 -- 加密后的密码传输）
def login(request):
    res = {'status':1,'message':'登陆成功'}
    body = json.loads(request.body.decode())
    user_name = body['user_name']
    print(body)
    result = models.Userinfo.objects.filter(user=user_name).values('user','passwd').first()
    if result == None:
        result = ''
    if len(result):
        if result['user'] == body['user_name'] and result['passwd'] == body['password']:
            res['message'] = '登陆成功'
        else:
            res['message'] = '密码错误'
            res['status'] = 0
    else:
        res['message'] = '账号不存在哦'
        res['status'] = 0
    return JsonResponse(res)



# 验证签名函数
def weixin_mainbak(request):
    if request.method == "GET":
        #接收微信服务器get请求发过来的参数
        signature = request.GET.get('signature', None)
        timestamp = request.GET.get('timestamp', None)
        nonce = request.GET.get('nonce', None)
        echostr = request.GET.get('echostr', None)
        print(signature,timestamp,echostr)
	    #服务器配置中的token
        token = '5HSw9hIXyRzygnK1xyNlSg'
        #把参数放到list中排序后合成一个字符串，再用sha1加密得到新的字符串与微信发来的signature对比，如果相同就返回echostr给服务器，校验通过
        hashlist = [token, timestamp, nonce]
        hashlist.sort()
        hashstr = ''.join([s for s in hashlist])
        hashstr = hashstr.encode('utf-8')
        hashstr = hashlib.sha1(hashstr).hexdigest()
        if hashstr == signature:
          return HttpResponse(echostr)
        else:
          return HttpResponse("field")
    else:
        pass
        # othercontent = autoreply(request)
        # return HttpResponse(othercontent)


# 手动获取ACEsstoken
def get_accesstoken(request):
    url  = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=wx71ccb0df8485c76a&secret=c84fa46393b54cf7e09d10fe7b2179d4'
    responce = requests.GET(url=url).text
    print(type(responce))
    print(json.loads(responce))
    return HttpResponse('nihao')

# 微信官方主函数
def weixin_main(request):
    str1 = """
    终于等到你！！！
快快添加咱们的机器宝宝吧~
查询优惠福利，更有免单派送哦！
扫码添加！马上领取！"""
    jieguo =  request.body
    data = ElementTree.XML(request.body.decode('utf-8'))
    open_id = data.find('FromUserName').text  # 用户open_id
    wxg_id = data.find('ToUserName').text  # 开发者微信号
    MsgType = data.find('MsgType').text
    if not MsgType == 'event':
        return HttpResponse()
    event = data.find('Event').text
    print('答题',event)
    print(open_id, wxg_id)
    print(type(open_id))
    ACCESS_TOKEN = get_accesstoken()
    print('asdsadasd',ACCESS_TOKEN)
    if not event == 'subscribe':
        return HttpResponse('')
    heihei2(open_id,ACCESS_TOKEN)
    heihei(open_id,ACCESS_TOKEN)

    #replyMsg = replyasd.TextMsg(open_id, wxg_id, str1)
    return HttpResponse()


def heihei(touser, ACCESS_TOKEN):
    url = 'https://api.weixin.qq.com/cgi-bin/message/custom/send?access_token=' + ACCESS_TOKEN
    print(123)
    record = int(models.Record.objects.filter(id=1).values('record')[0]['record'])
    image_id = models.TuPian.objects.filter(id=record).values('image_id')[0]['image_id']
    threshold = models.TuPian.objects.filter(id=record).values('threshold')[0]['threshold']
    thresholds = models.TuPian.objects.filter(id=record).values('thresholds')[0]['thresholds']
    if record == 20 and threshold == 5:
        models.TuPian.objects.filter(id=record).update(threshold=1)
        models.Record.objects.filter(id=1).update(record=1)
        models.TuPian.objects.filter(id=record).update(thresholds=thresholds + 1)
    elif record <= 20 and threshold < 5:
        models.TuPian.objects.filter(id=record).update(threshold=threshold + 1)
        models.TuPian.objects.filter(id=record).update(thresholds=thresholds + 1)
    else:
        models.Record.objects.filter(id=1).update(record=record + 1)
        models.TuPian.objects.filter(id=record).update(threshold=1)
        models.TuPian.objects.filter(id=record).update(thresholds=thresholds + 1)

    data = {
        "touser": touser,
        "msgtype": "image",
        "image":
            {
                "media_id": image_id
            }
    }
    data = json.dumps(data)
    response = requests.post(url, data=data)
    return response


def heihei2(touser,ACCESS_TOKEN):
    url = 'https://api.weixin.qq.com/cgi-bin/message/custom/send?access_token=' + ACCESS_TOKEN
    print(123)
    str1 = """终于等到你！！！
快快添加咱们的机器宝宝吧~
查询优惠福利，更有免单派送哦！
扫码添加！马上领取！"""
    data = {
        "touser": touser,
        "msgtype": "text",
        "text":
            {
                "content": str1
            }
    }
    #data = json.dumps(data)
    headers = {"Content-type": "application/json", "charset": "UTF-8"}
    r = requests.post(url=url, headers=headers,
                          data=bytes(json.dumps(data, ensure_ascii=False), encoding='utf-8'))

    return r.json()


