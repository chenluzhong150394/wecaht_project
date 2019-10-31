import os
import traceback

import xlrd
from django.shortcuts import render, HttpResponse, redirect
from django.http import FileResponse, JsonResponse
# from django.views import View
from website.datebase import *
from utils.transfer import Haproxy
from datetime import datetime
from rest_framework.views import APIView
import json
import threading
import datetime
from django.db.models import Q
# websocket
import shutil
from dwebsocket.decorators import accept_websocket
# 转账
from utils.read_excel import read_excel
from utils.payment_interface import Payment as Pay
from utils.update_pay_key import write_pay_key
from utils.read_pay_key import read_pay_key
from utils.yuancheng import Yuan


def init(request):
    return render(request, '../dist/../templates/index.html')


class Operationlog(APIView):
    """
    获取操作日志信息
    """

    def post(self, request):
        try:
            res = get_Operationlog()
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
            res = get_record(start_time, end_time, method)
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
        # pay = Pay(2018110661992863)
        pay = Pay()
        data = []
        # 记录一次转账的总钱数
        record_for_payment = 0.0
        count_for_succ = 0

        # 失败的总钱数
        record_for_unsucc = 0.0
        count_for_unsucc = 0

        # 判断是否重复转账 两天内
        # 当前日期
        now_date = datetime.datetime.now().strftime("%Y-%m-%d")
        yesterday_date = (datetime.datetime.today() + datetime.timedelta(-1)).strftime("%Y-%m-%d")
        payment_record = models.WebsitePayment.objects.filter(
            Q(pay_date__startswith=now_date) | Q(pay_date__startswith=yesterday_date)
        ).values('amount', 'payee_account', 'payee_real_name', 'remark').all()
        record_list = []
        for temp_record in payment_record:
            record_list.append(tuple(temp_record.values()))
        # 当前时间点 用于判断数据库写入是否完全
        now_date_time = datetime.datetime.now().strftime("%Y%m%d%H%M%S") + '0000'

        need_pay_queue = []
        check_pay_queue = []
        for item in file:
            need_pay_queue.append(tuple(item))
            check_pay_queue.append((str(item[0]), item[1], item[3], item[4]))

        duplicate_record = list(set(check_pay_queue) & (set(record_list)))
        if len(duplicate_record) > 0:
            res['message'] = "有重复转账记录："
            for item in duplicate_record:
                res['message'] += '\n 提现人:{} ,提现账号:{}, 提现金额:{}, 提现设备:{}'.format(item[2], item[1], item[0], item[3])
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

        # 判断数据是否写入完全
        new_payment_record = models.WebsitePayment.objects.filter(out_biz_no__gte=now_date_time).filter(
            ~Q(out_biz_no='no biz_no!!!!!!!')).all()
        if len(new_payment_record) == len(need_pay_queue) or error_update_counter == len(need_pay_queue):
            # 数据库写入完整
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


# 下载Excel
def get_excel(request):
    """
    调用下载器获取需要转账的表，
    :param request:
    :param operator 操作人
    :param uid 用户id
    :return: {'code': 0/1, 'message': error message, 'data': download message}
    """
    user_info = json.loads(request.body.decode())
    uid = int(user_info["uid"])
    # 取出操作人
    operator = models.WebsiteUserinfo.objects.filter(uid=uid).values('username').first()['username']
    print(operator)
    res = {'code': 0, 'message': "执行成功"}
    try:
        # delete old file
        new_path = r'C:\\Users\\Administrator\\Desktop\\backup_data\\'
        file_dir = r'C:\\Users\\Administrator\\Desktop\\record_joined_file\\joined_file.xls'
        os.remove(file_dir)
    except:
        pass
    download = Haproxy()  # 实例化下载器类
    t = threading.Thread(target=download.run)  # 开启线程调用run函数，下载Excel表格
    t.start()
    file_path = r'C:\\Users\\Administrator\\Desktop\\record_joined_file\\joined_file.xls'
    #读取转帐表，写入数据库
    try:
        res = read_excel(file_path)
        # [16.32, 'isabel98@163.com', '返利到账', '崔丹', '109']
        row = 0
        for i in res:
            money = i[0]
            zfb_number = i[1]
            device = i[-1]
            status = 0
            name = i[-2]
            models.WebsiteTranRecord.objects.create(money=money, name=name, zfb_number=zfb_number, device=device, status=status, operator=operator)
            row += 1
        now_time = time.strftime("%Y-%m-%d__%H:%M:%S", time.localtime()) + "写入数据库" +".xls"
        ## 引包 import shutil
        shutil.move(file_dir, new_path + now_time)
    except Exception as e:
        data = e.__repr__()
        res["code"] = 1
        res["message"] = data
        return JsonResponse(res)
    res["message"] = "成功写入了%s条待体现数据" % row
    return JsonResponse(res)


class Manager_review(APIView):
    """
    用户管理
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
    修改某个人的信息及权限
    """
    def post(self, request):
        id = request.data.get("uid", None)
        worker = models.WebsiteUserinfo.objects.filter(id=id).values('username').first()[
            'username']
        try:
            raw_auth = []
            raw_id = request.data.get('id', None)
            raw_username = request.data.get('username', None)
            raw_password = request.data.get('password', None)
            real_name = request.data.get('real_name', None)
            role = request.data.get('role', None)
            for power, values in request.data.get('power', None).items():
                if values:
                    raw_auth.append(models.WebsiteAuth.objects.filter(url=power).values('id').first()['id'])

            update_result = API().update_user(raw_id, raw_username, raw_password, raw_auth, real_name, role)
            if update_result:
                res = {'code': 0, 'message': raw_username + '的信息更新成功', 'data': []}
                write_log(worker, "修改了"+raw_username+"的信息及权限")
            else:
                res = {'code': 1, 'message': raw_username + '的信息更新失败', 'data': []}
        except Exception as e:
            res = {'code': 1, 'message': e.__repr__(), 'data': []}
        return JsonResponse(res)


class Remove_user(APIView):
    """
    删除用户
    """

    def post(self, request):
        try:
            id = request.data.get("uid", None)
            worker = models.WebsiteUserinfo.objects.filter(id=id).values('username').first()[
                'username']
            raw_id = request.data.get('id', None)
            user_name = models.WebsiteUserinfo.objects.filter(id=raw_id).values('username').first()[
                'username']
            remove_result = API().remove_user(raw_id)
            if remove_result:
                res = {'code': 0, 'message': user_name + '的信息删除成功', 'data': []}
                write_log(worker, "删除了用户"+user_name)
            else:
                res = {'code': 1, 'message': user_name + '的信息删除失败', 'data': []}
        except Exception as e:
            res = {'code': 1, 'message': e.__repr__(), 'data': []}
        return JsonResponse(res)


class Manager_user_auth(APIView):
    """
    新增用户
    """
    def post(self, request):
        id = request.data.get("uid", None)
        worker = models.WebsiteUserinfo.objects.filter(id=id).values('username').first()[
            'username']
        try:
            all_auth = API().get_auth_info()
            new_auth_list = []
            new_name = request.data.get('username', None)  # 新建用户用户名
            new_password = request.data.get('password', None)  # 新建用户密码
            real_name = request.data.get('real_name', None)  # 新建用户姓名
            role = request.data.get('role', None)  # 用户类型
            power = request.data.get('power', None)  # 用户权限
            for key, value in power.items():
                if value:
                    # 把用户全新更新到权限表中
                    new_auth_list.append(models.WebsiteAuth.objects.filter(url=key).values('id').first()['id'])
            # 判断用户是否存在
            current_user_list = API().get_all_user_name()
            if new_name not in current_user_list:
                # new user auth
                API().add_user(new_name, new_password, new_auth_list, real_name, role)
                res = {'code': 0, 'message': "添加成功", 'data': []}
                write_log(worker, "添加了新用户"+new_name)
            else:
                # change user auth
                res = {'code': 1, 'message': "已存在此用户", 'data': []}
        except Exception as e:
            res = {'code': 1, 'message': e.__repr__(), 'data': []}
        return JsonResponse(res)


def change_password(request):
    """
        修改密码
        接收: {token,uid,password:新密码}
        返回 : 默认
        """
    res = {'code': 0, 'message': "", 'data': []}
    user_id = eval(request.body).get('uid', None)
    worker = models.WebsiteUserinfo.objects.filter(id=user_id).values('username').first()['username']
    try:
        new_password = eval(request.body).get('password', None)
        models.WebsiteUserinfo.objects.filter(id=user_id).update(password=new_password)
        write_log(worker, '修改了密码')
        res['message'] = '密码修改成功'
    except Exception as e:
        res['code'] = 1
        res['message'] = '密码修改失败!' + e.__repr__()
    return JsonResponse(res)


def get_userinfo(request):
    """
        获取当前登录用户的信息
        接收: {token,uid}
        返回 : 默认
        """
    res = {'code': 0, 'message': "", 'data': {}}
    user_id = eval(request.body).get('uid', None)
    try:
        user = models.WebsiteUserinfo.objects.filter(id=user_id).first()
        role_dict = {"1": "管理员", "2": "普通"}
        user_info = {'name': user.name,
                     'role': role_dict[user.role],
                     'password': user.password,
                     'username': user.username,
                     }
        res['data'].update(user_info)
    except Exception as e:
        res['code'] = 1
        res['message'] = e.__repr__()
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


def update_pay_ses(request):
    """
    增加一个保存支付宝信息的接口
    :param request:
    :return:
    """
    request_boby_dict = eval(request.body)
    worker = models.WebsiteUserinfo.objects.filter(id=request_boby_dict['uid']).values('username').first()['username']
    print(request.body.decode())
    dic_body = request.body.decode()
    dic_body = json.loads(dic_body)
    # print(json.loads(request.body))
    public = dic_body.get('pub')
    private = dic_body.get('prv')
    appid = dic_body.get('appid')
    # print(public,private,appid)
    print(type(appid), type(public), type(private))
    res = write_pay_key(public, private, appid)
    if res == '写入成功':
        write_log(worker, '修改支付宝信息')
        return HttpResponse('支付宝商户信息保存成功')
    else:
        return HttpResponse(res)


def Read_pay_key(request):
    """
    获取支付宝接口信息
    :param request:
    :return:
    """
    request_boby_dict = eval(request.body)
    worker = models.WebsiteUserinfo.objects.filter(id=request_boby_dict['uid']).values('username').first()['username']
    if request.method == "POST":
        res = read_pay_key()
        write_log(worker, '获取支付宝信息')
        return JsonResponse(res)
    else:
        return HttpResponse('请求失败')


class Get_tran_monery(APIView):
    """
    主页获取金额信息
    """

    def post(self, request):
        try:
            res = get_tran_monery(request)
        except Exception as e:
            res = {'code': 1, 'message': e.__repr__(), 'data': []}
        return JsonResponse(res)


def get_device_information(request):
    """
    检测设备信息
    :param request:
    :return: {'code': 0, 'message': '', 设备总数量/'count': 0, 正常运行设备数量/'count1': 0, 异常设备数量/'count2': 0, 'data': [设备相关信息]}
    """
    res = {'code': 0, 'message': '', 'count': 0, 'count1': 0, 'count2': 0, 'data': []}
    try:
        info = models.Device_Information.objects.all()
        b = models.Device_Information.objects.filter(
            Q(software_status=0) & Q(wechat_status=0)).all()
        count = 0
        count1 = 0
        for i in info:
            count += 1
            res['data'].append({"id": i.id, "server": i.server, "device": i.device,
                                "software_account": i.software_account,
                                "wechat_id": i.wechat_id,
                                "software_status": i.software_status,
                                "wechat_status": i.wechat_status,
                                "test_time": i.test_time,
                                "remarks_information": i.remarks_information})
        res["count"] = count
        for _ in b:
            count1 += 1
        res["count1"] = count1
        res["count2"] = count - count1
    except Exception as e:
        res['code'] = 1
        res['message'] = e.__repr__()
    return JsonResponse(res)


def write_device_information(request):
    """
    写入检测设备信息
    :param request:
    :return:
    """
    request = request.body.decode()
    request = json.loads(request)
    robot_total = request['robot_total']
    we_total = request['we_total']
    time = request["test_time"]
    # 软件账号是个字典
    software_account = request['software_account']
    server_ip = request['serverIP']
    print(robot_total, we_total, software_account, server_ip, time)
    info = models.Device_Information.objects.filter(server=server_ip)
    for i in info:
        if i.software_account in software_account and robot_total == 2 and we_total == 2:
            i.software_status = 0
            i.wechat_status = 0
            i.test_time = time
            i.save()
        else:
            i.software_status = 1
            i.wechat_status = 1
            i.test_time = time
            i.save()
    return HttpResponse('写入成功')


# 这是检测设备的接口,首先获取IP列表，传入IP列表并使用远程调用函数批量执行服务器脚本，sshd的参数都是固定的，
def run_device_state(request):
    host_list = []
    res = {'code': 0, 'message': ""}
    try:
        result = models.Device_Information.objects.values('server').distinct().order_by('server')
        print(result)
        for i in result:
            ip = i["server"]
            host_list.append(ip)
        print(host_list)
        yuan = Yuan(host_list)
        t = threading.Thread(target=yuan.run)  # 开启调用执行远程函数
        t.start()
        res["message"] = '检测成功'
    except Exception as e:
        res = {'code': 1, 'message': e.__repr__()}
    return JsonResponse(res)


class Get_tran_record(APIView):
    """
    今日提现信息
    """

    def post(self, request):
        id = request.data.get("uid", None)
        worker = models.WebsiteUserinfo.objects.filter(id=id).values('username').first()[
            'username']
        try:
            res = get_tran_record(request)
            write_log(worker, '查看今日提现信息')
        except Exception as e:
            res = {'code': 1, 'message': e.__repr__(), 'data': []}
        return JsonResponse(res)


class Get_tran_record1(APIView):
    """
    获取转账信息接口
    """

    def post(self, request):
        id = request.data.get("uid", None)
        worker = models.WebsiteUserinfo.objects.filter(id=id).values('username').first()[
            'username']
        try:
            method = request.data.get('type', None)
            res = get_tran_record1(method)
            write_log(worker, "查看了转账信息")
        except Exception as e:
            res = {'code': 1, 'message': e.__repr__(), 'data': []}
        return JsonResponse(res)


class Get_tran_record2(APIView):
    """
    获取待处理提现信息
    """

    def post(self, request):
        id = request.data.get("uid", None)
        worker = models.WebsiteUserinfo.objects.filter(id=id).values('username').first()[
            'username']
        try:
            res = get_tran_record2(request)
            write_log(worker, '查看了待处理提现信息')
        except Exception as e:
            res = {'code': 1, 'message': e.__repr__(), 'data': []}
        return JsonResponse(res)


class Updata_tran_record(APIView):
    """
    修改待处理提现信息
    """

    def post(self, request):
        id = request.data.get("uid", None)
        worker = models.WebsiteUserinfo.objects.filter(id=id).values('username').first()[
            'username']
        try:
            result = updata_tran_record(request)
            res = {'code': 0, 'message': result}
            write_log(worker, '修改了待提现信息')
        except Exception as e:
            res = {'code': 1, 'message': e.__repr__()}
        return JsonResponse(res)


def balance_deposit(request):
    """
    存钱余额
    :param request:
    :return:｛'code': 0/1, 'message': error message,'data':{} }
    """
    res = {'code': 0, 'message': "", 'data': {}}
    request_boby_dict = eval(request.body)
    worker = models.WebsiteUserinfo.objects.filter(id=request_boby_dict['uid']).values('username').first()['username']
    try:
        deposit = float(eval(request.body).get('deposit', None))
        balance = models.Balance_Information.objects.order_by("-id").values('balance').first()['balance']
        balance_record = {'balance': round(balance + deposit, 2),
                          'time': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                          "balance_change": "+" + str(deposit)}
        models.Balance_Information.objects.create(**balance_record)
        res['message'] = '存款成功' + "+" + str(deposit)
        write_log(worker, '存入余额' + str(deposit) + "元")
    except Exception as e:
        res['code'] = 1
        res['message'] = '存款失败!' + e.__repr__()
    return JsonResponse(res)


def balance_preview(request):
    """
    查看余额
    :param request:
    :return:｛'code': 0/1, 'message': error message,'data':{} }
    """
    res = {'code': 0, 'message': "", 'data': {}}
    try:
        balance = models.Balance_Information.objects.values('balance').order_by('-id').first()['balance']
        res['data'] = balance
    except Exception as e:
        res['code'] = 1
        res['message'] = '余额查看失败!' + e.__repr__()
    return JsonResponse(res)
