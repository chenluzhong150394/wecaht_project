import os
import sqlite3
import shutil
import traceback
import xlrd
from django.shortcuts import render, HttpResponse, redirect
from django.http import FileResponse, JsonResponse
# from django.views import View
from website import models
from OA import settings
from .utils1 import create_mch_billno
from website.datebase import *
from utils.transfer import Haproxy
from datetime import datetime
from rest_framework.views import APIView
import json
import threading
import datetime
from django.db.models import Q
import hashlib
import requests
from utils import test
import requests
from xml.etree import ElementTree

list1 = ['TQUI51nP3YR5J8OZdMCSivqRI5igK15NGvdjUXsODSo', 'TQUI51nP3YR5J8OZdMCSil7bMwLskOLvFP9l4YQLHQ4', 'TQUI51nP3YR5J8OZdMCSijzTkEopkPy_c_uEHNMHR1c', 'TQUI51nP3YR5J8OZdMCSisZ2EA89vq39S7GOaPhj4XI', 'TQUI51nP3YR5J8OZdMCSiqve8pwMeQeMobHhyFro_yc', 'TQUI51nP3YR5J8OZdMCSitAfyaZGWG4NsN2P9ZnL5y4', 'TQUI51nP3YR5J8OZdMCSihKLumbIZZY85ywyDFhgocs', 'TQUI51nP3YR5J8OZdMCSinIrrKVygYMb8ppWP-cQSmQ', 'TQUI51nP3YR5J8OZdMCSil9A9FdaL_Svb8fo6pVa7ck', 'TQUI51nP3YR5J8OZdMCSit5UQtdF3E44lIOxkzk3tt8', 'TQUI51nP3YR5J8OZdMCSivnnQmlIIdjgGt-9XbBrNk0', 'TQUI51nP3YR5J8OZdMCSikJ-2vDdXdwde_RT-Bfpjxw']


# while True:
#     time_now = time.strftime("%S", time.localtime())  # 刷新
#     if time_now == '55':  # 此处设置每天定时的时间
#         # 此处3行替换为需要执行的动作
#         print("hello")
#         subject = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + " 定时发送测试"
#         print(subject)
#         time.sleep(2)  # 因为以秒定时，所以暂停2秒，使之不会在1秒内执行多次


from utils.test import *
# 测试
def test(request):
    print(get_info('o3L5YuPtvki2sjXFsqZpek_uLzi8'))

    return HttpResponse('123')


def regester_user(request):
    body = json.loads(request.body.decode())
    username = body['username']
    password = body['password']
    role = body['role']
    return HttpResponse('sad')



# 获取所有的关注者openID 并存入数据库中
def get_all_user(request):
    pass
    return HttpResponse('执行成功')

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


def write_tran_record(request):
    """
    接收远程服务器中的提现信息
    :param request: {number:提现信息数量, device:设备号,data:[[金额,支付宝,姓名],[金额,支付宝,姓名]]}
    :return: 返回1 表示接收并写入成功, 返回0 表示接收或写入失败
    """
    print('铁牛时代转账系统开始接收处理数据')
    try:
        request_boby_dict = eval(request.body)
        number = request_boby_dict["number"]
        device = request_boby_dict["device"]
        data1 = request_boby_dict["data"]
        n = 0
        status = 0
        mch_id = settings.WEINXIN_PAY_MCH_ID
        mch_billno = create_mch_billno(mch_id)
        if device == '099':
            device = 99
        if device == "祖师":
            device = 888
        if device == "祖母":
            device = 999
        for i in data1:
            models.TransferRecord.objects.create(name=i[2], re_openid=i[1], mch_billno=mch_billno,
                                                 device=device, total_amount=i[0], status=status)
            n += 1
        print(str(device) + "推送提现数据" + str(number) + "条")
        print("接收到" + str(device) + "提现数据" + str(n) + "条")
        res = 0
    except Exception as e:
        print(e.__repr__())
        res = 1
    return HttpResponse(res)

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

def get_accesstoken(request):
    url  = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=wx71ccb0df8485c76a&secret=c84fa46393b54cf7e09d10fe7b2179d4'
    responce = requests.GET(url=url).text
    print(type(responce))
    print(json.loads(responce))
    return HttpResponse('nihao')

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
    ACCESS_TOKEN = models.Token.objects.filter(id=1).values('token')[0]['token']
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


