import os
import traceback

import xlrd
from django.shortcuts import render, HttpResponse, redirect
from django.http import FileResponse, JsonResponse
# from django.views import View
from website.datebase import *
from utils.time_tools import day, month, time_list
from utils.transfer import Haproxy
from datetime import datetime
from rest_framework.views import APIView
import json
import threading
import datetime
# websocket
from dwebsocket.decorators import accept_websocket

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger, InvalidPage
# 转账
from utils.read_excel import read_excel
from utils.payment_interface import Payment as Pay
from utils.pay_record import Write_Payment_record
from utils.update_pay_key import write_pay_key

def init(request):
    return render(request, '../dist/../templates/index.html')


"""
    增加一个保存支付宝信息的接口

"""
def update_pay_ses(request):
    print(request.body.decode())
    dic_body = request.body.decode()
    dic_body = json.loads(dic_body)
    # print(json.loads(request.body))
    public = dic_body.get('pub')
    private = dic_body.get('prv')
    appid = dic_body.get('appid')
    # print(public,private,appid)
    print(type(appid),type(public),type(private))
    res = write_pay_key(public, private,appid)
    if res == '写入成功':
        return HttpResponse('支付宝商户信息保存成功')
    else:
        return HttpResponse(res)

"""
更新账户备注信息
"""
def Device_edit(request):
    # 更新设备信息
    try:
        request = json.loads(request.body)
        info = {}
        info['device'] = request.get('device' , None)
        info['account'] = request.get('account' , None)
        info['sequence'] = request.get('sequence' , None)
        info['wechat_id'] = request.get('wechat_id' , None)
        info['qq_id'] = request.get('qq_id' , None)
        info['phone_number'] = request.get('phone_number' , None)
        info['online_number'] = request.get('online_number' , None)
        info['remark'] = request.get('remark' , None)
        info['is_promoting'] = request.get('is_promoting' , None)
        info['pid_list'] = request.get('pid_list' , None)
        # req = eval(request.body.decode('utf-8'))
        res = update_device_info(info)
        #write_log(request.user, '修改设备信息'+req)
    except Exception as e:
        res = {'code': 1, 'message': e.__repr__(), 'data': {}}
    return JsonResponse(res)

class Device_review(APIView):
    """
    获取账户备注信息
    """

    def post(self, request):
        # 获取设备信息
        try:
            # req = eval(request.body.decode('utf-8'))
            res = get_device_info()
            # write_log(request.user, '查看设备信息'+req)
        except Exception as e:
            res = {'code': 1, 'message': e.__repr__(), 'data': {}}
        return JsonResponse(res)


def Device_add(request):
    # 更新设备信息
    try:
        # req = eval(request.body.decode('utf-8'))
        res = add_device()
        #write_log(request.user, '修改设备信息'+req)
    except Exception as e:
        res = {'code': 1, 'message': e.__repr__(), 'data': {}}
    return JsonResponse(res)

class Operationlog(APIView):
    """
    获取账户备注信息
    """

    def post(self, request):
        # 获取设备信息
        try:
            res = get_Operationlog()
            #write_log(request.user, '查看设备信息'+req)
        except Exception as e:
            res = {'code': 1, 'message': e.__repr__(), 'data': {}}
        return HttpResponse(json.dumps(res), content_type="application/json")





class Login(APIView):
    """
    用户登录
    """
    authentication_classes = []  # 此页面不需要认证，取消掉全局认证

    def post(self, request):
        username = request.data.get("username", None)
        password = request.data.get("password", None)
        # username = request.data['username']
        # password = request.data['password']
        res = login(username, password)
        write_log(username, '登陆')
        return JsonResponse(res, safe=False)






class PaymentRecord(APIView):
    """
    获取转账记录
    """
    def post(self, request):
        try:
            start_time = request.data.get('start_time', None)
            end_time = request.data.get('end_time', None)
            method = request.data.get('type', None)
            # status_type = request.data.get('status_type', None)
            res = get_record(start_time, end_time, method )
        except Exception as e:
            res = {'code': 1, 'message': e.__repr__(), 'data': []}
        return JsonResponse(res)

def download_excel(request):
    try:
        time.sleep(10)
        file_dir = 'C:\\Users\\Administrator\\Desktop\\record_joined_file\\joined_file.xls'
        file = open(file_dir, 'rb')
        # file = open('payment_all.xls', 'rb')
        response = FileResponse(file)
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename=' + datetime.datetime.now().strftime(
            "%Y-%m-%d %H-%M-%S") + '_joined_file.xls'

        return response
    except Exception as e:
        traceback.print_exc()
        return HttpResponse('出错啦！')

def upload_excel(request):
    """
    接收上传的文件
    :param request:
    :return:｛'code': 0/1, 'message': error message,'data':{} }
    """
    res = {'code': 0, 'message': "", 'data': {}}
    try:
        file = request.FILES.get('payment', None)
        f = open('backup/' + file.name, 'wb')
        for chunck in file.chunks():
            f.write(chunck)
        f.close()
        return JsonResponse(res)
    except Exception as e:
        res['code'] = 1
        res['message'] = '文件上传失败!' + e.__repr__()
        return JsonResponse(res)




class payment(APIView):
    def post(self, request):
        res = {'code': 0, 'message': "", 'data': []}
        # 读取上传的Excel文件的方式转账，上传成功后通过websocket连接就开始转账，并实时返回转账结果
        # 得到最新的xls表
        balance = models.WebsiteBalanceRecord.objects.order_by("-id").values('balance').first()['balance']
        print(balance)
        file_dir = u"backup/"
        file_list = os.listdir(file_dir)
        file_list.sort(key=lambda fn: os.path.getmtime(file_dir + fn) if not os.path.isdir(file_dir + fn) else 0)
        file = read_excel(file_dir + file_list[-1])  # 读取Excel表
        pay = Pay(2018110661992863)
        data = []
        # 记录一次转账的总钱数
        record_for_payment = 0.0
        count_for_succ = 0

        # 失败的总钱数
        record_for_unsucc = 0.0
        count_for_unsucc = 0

        #判断是否重复转账 两天内
        #当前日期
        now_date = datetime.datetime.now().strftime("%Y-%m-%d")
        yesterday_date = (datetime.datetime.today() + datetime.timedelta(-1)).strftime("%Y-%m-%d")
        payment_record = models.WebsitePayment.objects.filter(Q(pay_date__startswith=now_date) | Q(pay_date__startswith=yesterday_date)
        ).values('amount' , 'payee_account' , 'payee_real_name' , 'remark').all()
        record_list = []
        for temp_record in payment_record:
            record_list.append(tuple(temp_record.values()))
        #当前时间点 用于判断数据库写入是否完全
        now_date_time = datetime.datetime.now().strftime("%Y%m%d%H%M%S")+'0000'

        need_pay_queue = []
        check_pay_queue = []
        for item in file:
            need_pay_queue.append(tuple(item))
            check_pay_queue.append((str(item[0]) , item[1] , item[3], item[4]))


        duplicate_record = list(set(check_pay_queue) & (set(record_list)))
        if len(duplicate_record) > 0:
            res['message'] = "有重复转账记录："
            for item in duplicate_record:
                res['message'] += '\n 提现人:{} ,提现账号:{}, 提现金额:{}, 提现设备:{}'.format(item[2],item[1],item[0],item[3])
            res['code'] = 1
            return JsonResponse(res)
        # 开始转账
        error_update_counter = 0
        for item in need_pay_queue:
            rec = pay.pay(str(item[1]), item[0], item[3], item[2])
            rec['remark'] = item[4]
            if rec['status'] == '转账成功':
                count_for_succ += 1
                record_for_payment += float(rec['amount'])
                rec['first_pay_status'] = 1
                rec['success_time'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            else:
                rec['first_pay_status'] = 0
                count_for_unsucc += 1
                record_for_unsucc += float(rec['amount'])
            # 通过websocket返回转账结果
            try:  # 尝试读取第5列数据，如果没有则是新表，则将返回的数据直接写入到数据库中,否则为修改之后的表，更新原来的状态
                out_biz_no = item[5]
                rec['first_pay_status'] = 0
                rec['out_biz_no'] = out_biz_no
                if out_biz_no:
                    models.WebsitePayment.objects.filter(out_biz_no=out_biz_no).update(**rec)
                    error_update_counter += 1
                    data.append(rec)
            except Exception as e:
                # 此处并不是转账出错了
                data.append(rec)
                models.WebsitePayment.objects.create(**rec)

        #判断数据是否写入完全
        new_payment_record = models.WebsitePayment.objects.filter(out_biz_no__gte=now_date_time).filter(~Q(out_biz_no='no biz_no!!!!!!!')).all()
        if len(new_payment_record) == len(need_pay_queue) or error_update_counter == len(need_pay_queue):
            #数据库写入完整
            pass
        else:
            res['code'] = 1
            res['message'] = '数据库写入不完全'
        # 新增余额记录
        if record_for_payment > 0:
            balance_record = {'account_name': '铁牛5', 'balance': round(balance - record_for_payment, 2),
                              'update_time': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                              'last_time_balance': round(balance, 2), 'last_cost': round(record_for_payment, 2)}
            models.WebsiteBalanceRecord.objects.create(**balance_record)
        res['data'].extend(data)
        # res['data'].append({'order_unsucc': count_for_unsucc, 'amout_unsucc': round(record_for_unsucc, 2),
        #                     'order_succ': count_for_succ, 'amout_succ': round(record_for_payment, 2)})
        # Write_Payment_record(data)
        # print(data)
        return JsonResponse(res)


def balance_preview(request):
    """
    查看余额
    :param request:
    :return:｛'code': 0/1, 'message': error message,'data':{} }
    """
    res = {'code': 0, 'message': "", 'data': {}}
    try:
        balance = models.WebsiteBalanceRecord.objects.values('balance').order_by('-id').first()['balance']
        res['data'] = balance
    except Exception as e:
        res['code'] = 1
        res['message'] = '余额查看失败!' + e.__repr__()
    return JsonResponse(res)

def balance_deposit(request):
    """
    存钱余额
    :param request:
    :return:｛'code': 0/1, 'message': error message,'data':{} }
    """
    res = {'code': 0, 'message': "", 'data': {}}
    try:
        deposit = float(eval(request.body).get('deposit', None))
        balance = models.WebsiteBalanceRecord.objects.order_by("-id").values('balance').first()['balance']
        balance_record = {'account_name': '铁牛5', 'balance': round(balance + deposit, 2),
                          'update_time': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                          'last_time_balance': round(balance, 2), 'last_cost': -round(deposit, 2)}
        models.WebsiteBalanceRecord.objects.create(**balance_record)
        res['message'] = '存款成功'
    except Exception as e:
        res['code'] = 1
        res['message'] = '存款失败!' + e.__repr__()
    return JsonResponse(res)

# 下载Excel
@accept_websocket
def get_excel(request):
    """
    调用下载器获取转账表，通过websocket显示下载进度
    :param request:
    :return: {'code': 0/1, 'message': error message, 'data': download message}
    """
    res = {'code': 0, 'message': "", 'data': ""}
    if not request.is_websocket():  # 判断是不是websocket连接
        res['code'] = 1
        res['message'] = '请使用websocket连接访问'
        return JsonResponse(res)
    else:
        try:
            # delete old file
            file_dir = 'C:\\Users\\Administrator\\Desktop\\record_joined_file\\joined_file.xls'
            os.remove(file_dir)
        except:
            pass
        download = Haproxy()  # 实例化下载器类
        t = threading.Thread(target=download.run)  # 开启线程调用run函数，下载Excel表格
        t.start()
        sent = []
        while download.status:
            # 返回最新的几个下载结果
            if len(download.status_dict) > len(sent):
                count = 0
                for i in download.status_dict.keys():
                    if i not in sent:
                        count += 1
                        sent.append(i)
                for index in range(0 , count):
                    request.websocket.send(str(sent[len(sent)-index-1]+'@'+str(download.status_dict[sent[len(sent)-index-1]])).encode('utf-8'))   # 发送消息到客户端
        # request.websocket.send('下载完成'.encode('utf-8'))

class Manager_review(APIView):
    """
    查看用户信息
    """
    def post(self, request):
        try:
            res = get_all_user()
        except Exception as e:
            res = {'code': 1, 'message': e.__repr__(), 'data': []}
        return JsonResponse(res)

class Update_person_info(APIView):
    """
    修改某个人的信息权限
    """
    def post(self, request):
        try:
            raw_auth = []
            raw_id = request.data.get('id', None)
            raw_username = request.data.get('username', None)
            raw_password = request.data.get('password', None)
            real_name = request.data.get('real_name', None)
            group = request.data.get('group', None)
            for power , values in request.data.get('power', None).items():
                if values:
                    raw_auth.append(models.WebsiteAuth.objects.filter(url=power).values('id').first()['id'])

            update_result = API().update_user(raw_id , raw_username , raw_password , raw_auth ,real_name ,group)
            if update_result:
                res = {'code': 0, 'message': raw_username + '的信息更新成功', 'data': []}
            else:
                res = {'code': 1, 'message': raw_username + '的信息更新失败', 'data': []}
        except Exception as e:
            res = {'code': 1, 'message': e.__repr__(), 'data': []}
        return JsonResponse(res)

class Remove_user(APIView):
    """
    修改某个人的信息权限
    """
    def post(self, request):
        try:
            raw_id = request.data.get('id' , None)
            remove_result = API().remove_user(raw_id)
            if remove_result:
                res = {'code': 0, 'message': raw_id + '的信息删除成功', 'data': []}
            else:
                res = {'code': 1, 'message': raw_id + '的信息删除失败', 'data': []}
        except Exception as e:
            res = {'code': 1, 'message': e.__repr__(), 'data': []}
        return JsonResponse(res)

# 修改权限
class Manager_user_auth(APIView):
    """
    获取转账记录
    """
    def post(self, request):
        try:
            all_auth = API().get_auth_info()
            new_auth_list = []
            new_name = request.data.get('username',None)
            new_password = request.data.get('password' , None)
            real_name = request.data.get('real_name',None)
            group = request.data.get('group' , None)
            power = request.data.get('power' , None)
            for key , value in power.items():
                if value:
                    new_auth_list.append(models.WebsiteAuth.objects.filter(url=key).values('id').first()['id'])
            current_user_list = API().get_all_user_name()
            if new_name not in current_user_list:
                #new user auth
                API().add_user(new_name , new_password , new_auth_list  ,real_name , group)
                res = {'code': 0, 'message': "添加成功", 'data': []}
            else:
                #change user auth
                res = {'code': 1, 'message': "已存在此用户", 'data': []}
        except Exception as e:
            res = {'code': 1, 'message': e.__repr__(), 'data': []}
        return JsonResponse(res)

def change_password(request):
    """
        修改密码
        接收: {token,uid,
    	password :股东的密码
        }
        返回 : 默认
        """
    res = {'code': 0, 'message': "", 'data': []}
    user_id = eval(request.body).get('uid', None)
    worker = models.WebsiteUserinfo.objects.filter(id=user_id).values('username').first()['username']
    try:
        new_password = eval(request.body).get('password', None)
        models.WebsiteUserinfo.objects.filter(id=user_id).update(password = new_password)
        write_log(worker, '修改密码')
        res['message'] = '密码修改成功'
    except Exception as e:
        res['code'] = 1
        res['message'] = '密码修改失败!' + e.__repr__()
    return JsonResponse(res)


def get_userinfo(request):
    """
        获取某用户的信息
        接收: {token,uid,
    	password :股东的密码
        }
        返回 : 默认
        """
    res = {'code': 0, 'message': "", 'data': {}}
    user_id = eval(request.body).get('uid', None)
    # worker = models.WebsiteUserinfo.objects.filter(id=user_id).values('username').first()['username']
    try:
        # new_password = eval(request.body).get('password', None)
        user = models.WebsiteUserinfo.objects.filter(id=user_id).first()
        role_dict = {"1": "客服", "2": "管理员", "3": "超级管理员" , '4':'股东' , '5':'合伙人'}
        user_info = {'name':user.name,
            'group':role_dict[user.role],
            'password':user.password,
            'username':user.username,

        }
        # write_log(worker, '修改密码')
        res['data'].update(user_info)
    except Exception as e:
        res['code'] = 1
        res['message'] =  e.__repr__()
    return JsonResponse(res)





class get_device_state(APIView):
    """
    设备状态
    """
    def post(self, request):
        request_month = request.data.get('date', None)
        if request_month :  # 修改
            res = review_device_state(request_month)
        else:
            res = {'code': 1, 'message': '传入数据有误！', 'data': {}}
        return JsonResponse(res)


def set_device_state(request):
    """
    修改设备状态
        接收: {token , uid  ,eid , state , date , remark}
    返回: {code , message ,
    data:[
        {}
    ]
    """
    res = {'code': 0, 'message': "", 'data': []}
    uid = eval(request.body).get('uid', None)
    worker = models.WebsiteUserinfo.objects.filter(id=uid).values('username').first()['username']
    try:
        request = eval(request.body)
        try:
            edit_data = request['data']
            for item in edit_data:
                res = update_device_state(item)
            write_log(worker, '修改设备状态')
        except:
            res = {'code': 1, 'message': '传入数据有误！', 'data': {}}
        # res['data'] = balance
    except Exception as e:
        res['code'] = 1
        res['message'] = '设备查看失败!' + e.__repr__()
    return JsonResponse(res)











def download_log(request):
    """
    记录下载log
            接收: {token , uid , reserve_id ,}
        返回: {code , message ,
        data:[
            {}
        ]
    """
    res = {'code': 0, 'message': "", 'data': []}
    request_boby_dict = eval(request.body)
    worker = models.WebsiteUserinfo.objects.filter(id=request_boby_dict['uid']).values('username').first()['username']
    try:
        request_boby_dict['user_name'] = worker
        if 'start_time' not in request_boby_dict.keys():
            request_boby_dict['start_time'] = datetime.datetime.now().strftime('%Y-%m-%d')
        if 'end_time' not in request_boby_dict.keys():
            request_boby_dict['end_time'] = datetime.datetime.now().strftime('%Y-%m-%d')
        if 'type' not in request_boby_dict.keys():
            request_boby_dict['type'] = 'payment_all'
        request_boby_dict.pop('token')
        models.WebsiteDownloadLog.objects.create(**request_boby_dict)

        res['message'] = '下载表格记录成功'
    except Exception as e:
        res['code'] = 1
        res['message'] = '下载表格记录失败!' + e.__repr__()
    return JsonResponse(res)







def get_accounts(request):
    """
    获取设备账号
            接收: {token , uid }
        返回: {code , message ,
        data:[
            {}
        ]
    """
    res = {'code': 0, 'message': "", 'data': []}
    try:
        account_list = models.WebsiteDevice.objects.filter().values('account').all().distinct()
        for account in account_list:
            res['data'].append(account['account'])
    except Exception as e:
        res['code'] = 1
        res['message'] = '账号查看失败!' + e.__repr__()
    return JsonResponse(res)

def get_all_devices(request):
    """
    获取设备号
            接收: {token , uid }
        返回: {code , message ,
        data:[
            {}
        ]
    """
    res = {'code': 0, 'message': "", 'data': []}
    try:
        device_list = models.WebsiteDevice.objects.filter().values('device').all().distinct()
        for device in device_list:
            res['data'].append({'device':device['device']})
    except Exception as e:
        res['code'] = 1
        res['message'] = '账号查看失败!' + e.__repr__()
    return JsonResponse(res)





def Preview_SH_own_devices(request):
    """
    查看股东拥有设备号
            接收: {token , uid , id(指定股东的id)}
        返回: {code , message ,
        data:[
            {}
        ]
    """
    res = {'code': 0, 'message': "", 'data': []}
    sh_id = eval(request.body).get('id' , None)
    try:
        SH_devices = models.WebsiteShareholderinfo.objects.filter(sh_id=sh_id).first().own_devices.all()
        for item in SH_devices:
            device_info = {'device': item.device, 'account': item.account,  'sequence': item.sequence,
                                'wechat_id': item.wechat_id, 'qq_id': item.qq_id, 'phone_number': item.phone_number,
                                'online_number': item.online_number, 'remark': item.remark , 'is_promoting':item.is_promoting , 'eid':item.id}
            res['data'].append(device_info)
        # balance = models.WebsiteBalanceRecord.objects.values('balance').order_by('-id').first()['balance']
        # res['data'] = balance
    except Exception as e:
        res['code'] = 1
        res['message'] = '设备查看失败!' + e.__repr__()
    return JsonResponse(res)

def Add_device(request):
    """
    增加设备
    接收: {token,uid,
	id :股东的id,
	eids:[ ] //新增的设备的eid
    }
    返回 : 默认
    """
    res = {'code': 0, 'message': "", 'data': []}
    sh_id = eval(request.body).get('id' , None)

    try:
        add_devices_id = eval(request.body).get('eids', None)
        SH = models.WebsiteShareholderinfo.objects.filter(sh_id=sh_id).first()
        for eid in add_devices_id:
            SH.own_devices.add(eid)
            models.WebsiteDevice.objects.filter(id = eid).update(is_distributed = 1)
        res['message'] = '设备添加成功'
    except Exception as e:
        res['code'] = 1
        res['message'] = '设备添加失败!' + e.__repr__()
    return JsonResponse(res)

def Del_device(request):
    """
    删除股东所属设备
    接收: {token,uid,
	id :股东的id,
	eids:[ ] //删除的设备的eid
    }
    返回 : 默认
    """
    res = {'code': 0, 'message': "", 'data': []}
    sh_id = eval(request.body).get('id' , None)
    del_devices_id = eval(request.body).get('eids', None)
    try:
        SH = models.WebsiteShareholderinfo.objects.filter(sh_id=sh_id).first()
        if del_devices_id:
            SH.own_devices.remove(del_devices_id)
            models.WebsiteDevice.objects.filter(id=del_devices_id).update(is_distributed=0)
        # SH_devices = models.WebsiteShareholderinfo.objects.filter(SH_id=sh_id).first().own_devices.all()
        # for item in SH_devices:
        #     res['data'].append(item.device)
        # balance = models.WebsiteBalanceRecord.objects.values('balance').order_by('-id').first()['balance']
        res['message'] = '设备删除成功'
    except Exception as e:
        res['code'] = 1
        res['message'] = '设备删除失败!' + e.__repr__()
    return JsonResponse(res)

def add_cost(request):
    """
    增加成本
    接收: {token,uid,month,cost_manpower,cost_rent,cost_device
    }
    返回 : 默认
    """
    res = {'code': 0, 'message': "", 'data': []}
    operator_id = eval(request.body).get('uid', None)
    month = eval(request.body).get('month' , None)
    cost_manpower = eval(request.body).get('cost_manpower' , None)
    cost_rent = eval(request.body).get('cost_rent' , None)
    cost_device = eval(request.body).get('cost_device' , None)
    cost_id = eval(request.body).get('cost_id' , None)
    cost_all = eval(request.body).get('cost_all' , None)
    type = eval(request.body).get('type' , None)
    try:
        if type == 0 and not cost_id:
            method = '新增'
            month_cost = {'month':month,
                          'employee_wages':cost_manpower,
                          'rent':cost_rent,
                          'device_cost':cost_device,
                          'cost_all':cost_all,
                          }
            if month:
                models.WebsiteMonthCost.objects.create(**month_cost)
            res['message'] = month + '成本' +  method + '成功'
        elif type == 1 and cost_id:
                method = '修改'
                month_cost = {'month': month,
                              'employee_wages': cost_manpower,
                              'rent': cost_rent,
                              'device_cost': cost_device,
                              'cost_all': cost_all,
                              }
                if month:
                    models.WebsiteMonthCost.objects.filter(id=cost_id).update(**month_cost)
                res['message'] = month + '成本' + method + '成功'
    except Exception as e:
        res['code'] = 1
        res['message'] = month + '成本' +  method + '失败' + e.__repr__()
    return JsonResponse(res)

def preview_cost(request):
    """
    预览成本
    接收: {token,uid
    }
    返回 : 默认
    """
    res = {'code': 0, 'message': "", 'data': []}
    try:
        month_costs = models.WebsiteMonthCost.objects.all()
        for query in month_costs:

            month_cost_record = {'month':query.month,
                          'employee_wages':query.cost_manpower,
                          'cost_rent':query.cost_rent,
                          'cost_device':query.device_cost,
                          }
            res['data'].append(month_cost_record)
    except Exception as e:
        res['code'] = 1
        res['message'] = month + '成本添加失败' + e.__repr__()
    return JsonResponse(res)








