import calendar
import copy

from website import models
from django.db.models import Sum
from django.db.models import Avg
from django.db import transaction
from utils.time_tools import time_list, day
from datetime import datetime
from dateutil.relativedelta import relativedelta
import re
import json
import hashlib
import time
import datetime
from django.db.models import Q
from utils.payment_interface import Payment as Pay
from django.db.models import Count
from django.forms.models import model_to_dict
import traceback
from django.core import serializers


def create_token(username):
    """
    生成token，用户登录成功后返回token，下次访问需要携带token验证用户信息
    :param username: 用户名
    :return: token
    """
    ctime = str(time.time())
    m = hashlib.md5(bytes(username, encoding='utf-8'))
    m.update(bytes(ctime, encoding='utf-8'))
    return m.hexdigest()


def login(username, password):
    """
    登录验证
    :param username: 用户名
    :param password: 密码
    :return: token data{权限}
    """
    res = {'code': 0, 'message': "", 'data': {}}
    try:
        # 获取用户对象
        userinfo = models.WebsiteUserinfo.objects.filter(username=username).first()
        print(userinfo)
        if userinfo:
            if password == userinfo.password:
                # 登陆成功生成token保存并返回(以后每次请求都需携带这个token验证)
                token = create_token(username)
                models.WebsiteUserinfo.objects.filter(username=username).update(token=token)
                res['data']['token'] = token
                res['data']['role'] = userinfo.role  # 用户角色信息
                res['data']['uid'] = userinfo.id
                auth = {}.fromkeys([n.url for n in models.WebsiteAuth.objects.all()], False)  # 获取用户拥有的权限
                for i in userinfo.userauth.all():
                    auth[i.url] = True
                res['data']['auth'] = auth
                return res
            else:
                res['code'] = 1
                res['message'] = '密码错误'
                return res
        else:
            res['code'] = 1
            res['message'] = '当前用户不存在'
            return res
    except Exception as e:
        res['code'] = 1
        res['message'] = e.__repr__()
        return res


# 单次转帐接口
def pay_one(request):
    req = json.loads(request.body.decode())
    # 查询数据库中的余额
    balance = int(models.Balance_Information.objects.order_by("-id").values('balance').first()['balance'])
    print(balance)
    # payee_account, amount, id, payee_real_name
    # (金额, 账号, 姓名, id, 设备名)
    id = req['id']
    te_order = models.WebsiteTranRecord.objects.filter(id=id).values("money", "zfb_number", "name", "id", "device")[0]
    res = {'code': 0, 'message': "", 'data': []}
    data_list = []
    for key, vaules in te_order.items():
        data_list.append(vaules)
    data_tuple = tuple(data_list)
    # 取出要进行转账的用户信息与金额
    pay = Pay()
    # (1.2, '2245966773@qq.com', '陈露中', 1, '12号')
    # payee_account, amount, id, payee_real_name = None, remark = None,
    rec = pay.pay(data_tuple[1], data_tuple[0], data_tuple[3], data_tuple[2], "返利到账")
    rec['remark'] = data_tuple[4]
    cout = 0
    if rec['status'] == '转账成功':
        rec['success_time'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        models.WebsiteTranRecord.objects.filter(id=id).update(status=3, pay_date=rec["pay_date"],
                                                              order_id=rec['order_id'], out_biz_no=rec['out_biz_no'],
                                                              remark=rec["status"])
        print("更新数据库成功")
        cout += 1
        res = {'code': 0, 'message': "转帐成功", 'data': {}}
    else:
        now_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        models.WebsiteTranRecord.objects.filter(id=id).update(status=2, remark=rec['status'],
                                                              out_biz_no=rec['out_biz_no'])
        shibai = rec['status']
        res = {'code': 1, 'message': shibai, 'data': {}}
    # # 新增余额记录

    if cout > 0:
        balance2 = '-' + str(round(data_tuple[0], 2))
        balance_record = {'balance': round(balance - data_tuple[0], 2),
                          'time': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                          'balance_change': balance2, 'status': 1}
        models.Balance_Information.objects.create(**balance_record)

    return res


# def get_record(start_time, end_time, method='payment_all'):
#     """
#     获取转账记录
#     :param start_time: 开始时间
#     :param end_time:  结束时间
#     :param method: 记录类型（默认全部）
#
#     :return: {'code':0/1, 'message': error message ,\
#                 'data':[{'amount':  ,'account':  ,'name':  ,'remark':  , 'out_biz_no':  ,'status':  }, {   },  {   } ]}
#     """
#     res = {'code': 0, 'message': "", 'data': []}
#     first_pay_status_dict = {'first_succ': 1, 'no_first_succ': 0, }
#     try:
#         # 没有传递参数默认显示当天数据
#         if not start_time or not end_time:
#             end_time = datetime.datetime.now().strftime("%Y-%m-%d")
#             start_time = end_time
#
#         # 前端传递的时间格式为2018-08-08，由于数据库里面时通过order_id字段查询时间格式为20180808，需要处理时间格式
#         # 因为要比较outbizno 后面增加10个0
#         start_time = start_time.replace('-', '') + '0' * 10
#         end_time = end_time.replace('-', '') + '9' * 10
#         # 查询所有的转账记录
#         if method == 'payment_all':
#             info = models.WebsitePayment.objects.filter(out_biz_no__gte=start_time).filter(
#                 out_biz_no__lte=end_time).all()
#         # 查询转账失败记录(已补交和未补缴)的记录
#         elif method == 'payment_fail':
#             info = models.WebsitePayment.objects.filter(out_biz_no__gte=start_time).filter(
#                 out_biz_no__lte=end_time, first_pay_status=first_pay_status_dict['no_first_succ']).all()
#         # 待补交(未补缴)
#         else:
#             info = models.WebsitePayment.objects.filter(out_biz_no__gte=start_time).filter(
#                 out_biz_no__lte=end_time, first_pay_status=first_pay_status_dict['no_first_succ']).exclude(
#                 status='转账成功').all()
#
#         for i in info:
#             res['data'].append(
#                 {'amount': i.amount, 'account': i.payee_account, 'name': i.payee_real_name, 'remark': i.remark,
#                  'out_biz_no': i.out_biz_no, 'status': i.status, 'first_pay_status': i.first_pay_status,
#                  'pay_date': i.pay_date})
#
#     except Exception as e:
#         res['code'] = 1
#         res['message'] = e.__repr__()
#
#     return res


def write_log(username, record):
    """
    记录用户操作日志
    :param username: 用户名
    :param record: 操作内容
    :return: None
    """
    try:
        models.WebsiteLog.objects.create(username=username, record=record)
    except Exception as e:
        return


def get_user_id(username):
    if username:
        return models.WebsiteUserinfo.objects.filter(username=username).first().id


class API(object):
    """
    所有用户信息获取接口
    """

    def __init__(self):
        self.res = {'code': 0, 'message': '', 'data': {}}

    def get_group_info(self):
        """
        返回全部用户组权限信息
        :return: [{'name':groupname, 'auth':[1,2,3....]}....]
        """
        data = models.WebsiteGroup.objects.all()
        for d in data:
            d.auth = [{'id': i.id, 'name': i.name} for i in d.groupauth.all()]
        info = []
        for a in data:
            info.append({'name': a.groupname, 'auth': a.auth})

        self.res['data'] = info
        return self.res

    def get_user_url(self, name):
        """
        获取用户的拥有的url
        :param name: 用户名
        :return: ['url','url'...] /false
        """
        data = models.WebsiteUserinfo.objects.filter(username=name).first()
        res = []
        if data:
            for i in data.userauth.all():
                for u in re.split('[,， ]', i.url):
                    res.append(u)
            return res
        else:
            return False

    def get_all_user_name(self):
        """
        获取用户的拥有的url
        :param none
        :return: ['root','admin'...] /false
        """
        data = models.WebsiteUserinfo.objects.values_list('username').distinct()
        if data:
            res = [i[0] for i in data]
            return res
        else:
            return False

    def get_user_aid(self, name):
        """
        获取用户权限id
        :param name: 用户名
        :return: '1234'/false
        """
        data = models.WebsiteUserinfo.objects.filter(username=name).first()
        res = ""
        if data:
            for i in data.userauth.all():
                res += str(i.id)
                res += ','
            self.res['data'] = res
            return self.res
        else:
            return False

    def get_user_gid(self, name):
        """
        获取用户的gid
        :param name: 用户名
        :return: gid/false
        """
        data = models.WebsiteUserinfo.objects.filter(username=name).first()
        if data:
            self.res['data'] = data.gid.gid
            return self.res
        else:
            self.res['code'] = 1
            return self.res

    def get_user_group_info(self, name):
        """
        获取当前用户的用户组下的所有权限
        :param name: 用户名
        :return:[{'name': auth.name,'id':auth.id}...]
        """
        # 获取当前用户的用户组名
        data = models.WebsiteUserinfo.objects.filter(username=name).first()
        group = data.gid.groupname
        # 获取这个用户组的权限信息
        data = models.WebsiteGroup.objects.filter(groupname=group).first()
        auth = data.groupauth.all()
        data = []
        for a in auth:
            data.append({'name': a.name, 'id': a.id})
        self.res['data'] = data
        return self.res

    def get_auth_info(self):
        """
        获取所有权限信息
        :return: [{'name': authname, 'id': authid, 'title': authtitle, 'url': authurl},........]
        """
        info = []
        data = models.WebsiteAuth.objects.all()
        for d in data:
            info.append({'id': d.id, 'name': d.name, 'title': d.title, 'url': d.url})
        return info

    def update_usergroup(self, name, auth):
        """
        更新或新建用户组
        更新：当删除了某个权限，其下拥有此权限的用户也会删除这个权限
             增加权限，用户权限不变
        :param name: 用户组名称
        :param auth: 权限信息
        :return:true/false
        """
        try:
            # 判断是否已经存在当前用户组
            group = models.WebsiteGroup.objects.filter(groupname=name).first()
            # 如果存在则修改权限
            if group:
                # 获取当前用户组下的所有用户
                i = models.WebsiteUserinfo.objects.filter(gid__groupname=name).all()
                for u in i:
                    for a in u.userauth.all():
                        # 如果用户组的某个权限被删除了，其下拥有这个权限的用户此权限也会被删除
                        if a.id not in auth:
                            u.userauth.remove(a)

                group.groupauth.set(auth)
                return True
            # 否则新建一个用户组
            else:
                gid = models.WebsiteGroup.objects.last()  # 获取最后一个用户组的gid 实现自动加一
                models.WebsiteGroup.objects.create(groupname=name, gid=(gid.gid + 1))
                models.WebsiteGroup.objects.filter(groupname=name).first().groupauth.set(auth)
                return self.res
        except Exception as e:
            self.res['code'] = 1
            self.res['message'] = e.__repr__()
            return self.res

    def remove_group(self, name):
        """
        删除用户组，注意如果用户组中存在用户，那么删除用户组的同时，其下的所有用户也会被删除
        :param name: groupname
        :return:true/false
        """

        try:
            models.WebsiteGroup.objects.filter(groupname=name).delete()
            return True
        except Exception as e:
            self.res['code'] = 1
            self.res['message'] = e.__repr__()
            return self.res

    def remove_auth(self, name):
        """
        删除权限，所有用户的这个权限都会被删除
        :param name: 权限名
        :return: true/false
        """
        try:
            models.WebsiteAuth.objects.filter(name=name).delete()
            return True
        except Exception as e:
            print(e)
            return False

    def add_user(self, name, password, auth, real_name, role, sex='male'):
        # 增加新用户

        role_dict = {"管理员": "1", "客服": "2"}
        try:
            if models.WebsiteUserinfo.objects.filter(username=name):
                return False
            else:
                models.WebsiteUserinfo.objects.create(username=name, password=password, sex=sex,
                                                      role=role_dict[role], name=real_name).userauth.set(auth)
                return True

        except Exception as e:
            print(e)
            return False

    def remove_user(self, id):
        # 删除用户
        try:
            models.WebsiteUserinfo.objects.filter(id=id).delete()
            return True
        except Exception as e:
            return False

    def update_user(self, id, username, password, auth, real_name, role):
        """
        更新用户信息
        :param id:用户id
        :param username:登录名
        :param password: 密码
        :param auth: 权限
        :param real_name: 姓名
        :param role: 用户类型
        :return: true/false
        """
        role_dict = {"管理员": "1", "客服": "2"}
        try:
            data = models.WebsiteUserinfo.objects.filter(id=id)
            if data:
                data.update(password=password, username=username, name=real_name, role=role_dict[role])
                data.first().userauth.set(auth)
                return True
            else:
                return False

        except Exception as e:
            return False

    def update_auth(self, name, url):
        """
        更新或新建权限
        :param name: 标题
        :param url: 链接地址
        :return: true/false
        """
        try:
            data = models.WebsiteAuth.objects.filter(name=name)
            if data:
                data.update(url=url)
            else:
                models.WebsiteAuth.objects.create(name=name, url=url)
            return True

        except Exception as e:
            print(e)
            return False


def get_all_user():
    """
    获取所有用户
    :return:{'code': 0/1, 'message': error message, 'data':[ { }, {  }, {  }]}
    """
    res = {'code': 0, 'message': '', 'data': []}
    role_dict = {"1": "管理员", "2": "普通用户"}
    try:
        data = models.WebsiteUserinfo.objects.all()
        for i in data:
            # get all auth of user
            auth = {}.fromkeys([n.url for n in models.WebsiteAuth.objects.all()], False)  # 获取用户拥有的权限
            for j in i.userauth.all():
                auth[j.url] = True
            i.role = role_dict[i.role]
            res['data'].append(
                {'id': i.id, 'username': i.username, 'real_name': i.name, 'password': i.password, 'role': i.role,
                 'auth': auth})
    except Exception as e:
        res['code'] = 1
        res['message'] = e.__repr__()
    return res


def get_Operationlog():
    """
    获取所有操作日志
    :return:{'code': 0/1, 'message': error message, 'data':[ {'device':  'account':  }, {  }, {  }]}
    """
    res = {'code': 0, 'message': '', 'data': []}
    try:
        # 按照最近的时间查看
        data = models.WebsiteLog.objects.all().order_by('-time')[:100]
        for i in data:
            if i.time == None:
                continue
            else:
                i.time = datetime.datetime.strftime(i.time, "%Y-%m-%d %H:%M:%S")
            res['data'].append({'time': i.time, 'username': i.username, 'record': i.record})
    except Exception as e:
        res['code'] = 1
        res['message'] = e.__repr__()
    return res


# 获取主页金额相关信息
def get_tran_monery(request):
    res = {'code': 0, 'message': '', 'data': {}}
    try:
        a = models.WebsiteTranRecord.objects.filter(Q(status=1) | Q(status=3)).all()
        c = models.WebsiteTranRecord.objects.filter(status=0).all()
        balance = models.Balance_Information.objects.values('balance').order_by('-id').first()['balance']
        total = 0
        count = 0
        total1 = 0
        count1 = 0
        for i in a:
            total += i.money
            count += 1
        for i in c:
            total1 += i.money
            count1 += 1
        res["data"]["success_m"] = round(total, 2)
        res["data"]["success"] = count
        res["data"]["wait_m"] = round(total1, 2)
        res["data"]["wait"] = count1
        res["data"]["balance"] = round(balance, 2)
    except Exception as e:
        res['code'] = 1
        res['message'] = e.__repr__()
    return res


def get_tran_record(request):
    """
    获取今日提现相关信息
    :return:
    """
    res = {'code': 0, 'message': "", 'data': [], "data1": []}
    # 总设备列表
    count = []
    # 提现设备列表
    count1 = []
    # 提现金额
    monery = 0
    try:
        balance = models.Balance_Information.objects.values('balance').order_by('-id').first()['balance']
        info = models.Device_Information.objects.all()
        for i in info:
            count.append(i.device)
        info = models.WebsiteTranRecord.objects.filter(status=0).all()
        for i in info:
            monery += i.money
            count1.append(i.device)
        a = (len(count1))
        count1 = set(count1)
        len(count1)
        monery = round(monery, 2)
        res["data"].append(
            {"device_count": len(count), "cash_device_count": len(count1), "cash_count": a, "cash_monery": monery,
             "balance": balance})
        for i in info:
            res['data1'].append(
                {"id": i.id, 'monery': i.money, 'name': i.name, 'zfb': i.zfb_number,
                 'device': i.device, 'pay_date': i.pay_date, 'order_id': i.order_id,
                 'remake': i.remark, 'out_biz_no': i.out_biz_no, 'status': i.status, 'operator': i.operator})
    except Exception as e:
        res['code'] = 1
        res['message'] = e.__repr__()

    return res


def get_tran_record1(start_time, end_time, method):
    """
    获取转账记录
    :param start_time: 开始时间
    :param end_time:  结束时间
    :param method: 记录类型（默认全部）

    :return: {'code':0/1, 'message': error message ,\
                'data':[{'amount':  ,'account':  ,'name':  ,'remark':  , 'out_biz_no':  ,'status':  }, {   },  {   } ]}
    """
    res = {'code': 0, 'message': "", 'data': []}
    try:
        # 没有传递参数默认显示当天数据
        if not start_time or not end_time:
            end_time = datetime.datetime.now().strftime("%Y-%m-%d")
            start_time = end_time
        start_time = start_time.replace('-', '') + '0' * 10
        end_time = end_time.replace('-', '') + '9' * 10
        # 待补交(未补缴)
        if method == 'payment_fail':
            info = models.WebsiteTranRecord.objects.filter(out_biz_no__gte=start_time).filter(
                out_biz_no__lte=end_time).filter(status=2).all()
        # 查询转账失败记录(已补交和未补缴)的记录
        elif method == 'payment_fail1':
            info = models.WebsiteTranRecord.objects.filter(out_biz_no__gte=start_time).filter(
                out_biz_no__lte=end_time).filter(Q(status=2) | Q(status=3)).all()
        # 查询所有的转账记录
        else:
            info = models.WebsiteTranRecord.objects.filter(out_biz_no__gte=start_time).filter(
                out_biz_no__lte=end_time).exclude(status=0).all()

        for i in info:
            res['data'].append(
                {"id": i.id, 'monery': i.money, 'name': i.name, 'zfb': i.zfb_number,
                 'device': i.device, 'pay_date': i.pay_date, 'order_id': i.order_id,
                 'remake': i.remark, 'out_biz_no': i.out_biz_no, 'status': i.status, 'operator': i.operator})

    except Exception as e:
        res['code'] = 1
        res['message'] = e.__repr__()

    return res


def get_tran_record2(request):
    """
    获取待处理提现
    """
    res = {'code': 0, 'message': "", 'data': [], "data1": []}
    monery = 0
    count = 0
    try:
        balance = models.Balance_Information.objects.values('balance').order_by('-id').first()['balance']
        info = models.WebsiteTranRecord.objects.filter(Q(status=0) | Q(status=2)).all()
        for i in info:
            count += 1
            monery += i.money
            res['data1'].append(
                {"id": i.id, 'monery': i.money, 'name': i.name, 'zfb': i.zfb_number,
                 'device': i.device, 'pay_date': i.pay_date, 'order_id': i.order_id,
                 'remake': i.remark, 'out_biz_no': i.out_biz_no, 'status': i.status, 'operator': i.operator})
        res["data"].append({"count": count, "monery": round(monery, 2), "balance": balance})
    except Exception as e:
        res['code'] = 1
        res['message'] = e.__repr__()

    return res


def get_tran_record3(type, monery, name, zfb):
    """
    根据不同的类型筛选转账记录中符合的记录
    :param type: 类型
    :param monery: 金额
    :param name: 名字
    :param zfb: 支付宝账户
    :return: 返回的是数据库中符号条件的字段
    """

    res = {'code': 0, 'message': "", 'data': []}
    try:
        # 根据金额选
        if type == 'monery':
            info = models.WebsiteTranRecord.objects.filter(money=monery).exclude(status=0).all()
        # 根据姓名筛选
        elif type == 'name':
            info = models.WebsiteTranRecord.objects.filter(name=name).exclude(status=0).all()
        # 根据支付宝账号筛选
        else:
            info = models.WebsiteTranRecord.objects.filter(zfb_number=zfb).exclude(status=0).all()

        for i in info:
            res['data'].append(
                {"id": i.id, 'monery': i.money, 'name': i.name, 'zfb': i.zfb_number,
                 'device': i.device, 'pay_date': i.pay_date, 'order_id': i.order_id,
                 'remake': i.remark, 'out_biz_no': i.out_biz_no, 'status': i.status, 'operator': i.operator})

    except Exception as e:
        res['code'] = 1
        res['message'] = e.__repr__()

    return res


def updata_tran_record(request):
    """
    修改待提现信息
    :param request:
    :return:
    """
    id = request.data.get("id", None)
    monery = request.data.get("monery", None)
    name = request.data.get("name", None)
    zfb = request.data.get("zfb", None)
    if id:
        info = models.WebsiteTranRecord.objects.filter(id=id).all()
        for i in info:
            i.money = monery
            print(i.money)
            i.name = name
            i.zfb_number = zfb
            i.save()
        return "修改成功"
    else:
        return "修改失败"
