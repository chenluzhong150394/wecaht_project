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


def get_device_info():
    """
    获取所有账户设备信息
    :return:{'code': 0/1, 'message': error message, 'data':[ {'device':  'account':  }, {  }, {  }]}
    """
    res = {'code': 0, 'message': '', 'data': []}
    try:
        online_status_data = {}
        session_update_time_data = {}
        data = models.WebsiteDevice.objects.all().order_by('sequence')
        temp_data = models.OnlineStatua.objects.values_list('user_id', 'statua').all()
        for item in temp_data:
            online_status_data[item[0]] = item[1]

        temp_data = models.websiteDeviceSession.objects.values_list('device_name', 'datetime').all()
        for item in temp_data:
            session_update_time_data[item[0]] = item[1]
        for i in data:
            if '_' in i.account:
                i.account = i.account.split('_')[0]
            if i.account in online_status_data:
                online_status = online_status_data[i.account]
            else:
                online_status = ''

            try:
                if i.account in session_update_time_data:
                    # temp =
                    session_update_time = (datetime.datetime.strptime(session_update_time_data[i.account],
                                                                      '%Y-%m-%d %H:%M:%S') + datetime.timedelta(
                        days=30)).strftime('%Y-%m-%d %H:%M:%S')
                else:
                    session_update_time = ''
            except:
                session_update_time = ""
            if i.is_distributed == 1:
                sh_id = models.WebsiteShareholderinfo.objects.filter(own_devices=i.id).values('sh_id').first()
                if sh_id:
                    sh_id = sh_id['sh_id']
                    belong_to_whom = models.WebsiteUserinfo.objects.filter(id=sh_id).values('name').first()['name']
            else:
                belong_to_whom = '公司'
            if i.is_promoting == 1:
                is_promoting = '正在推广中'
            elif i.is_promoting == 0:
                is_promoting = '完成推广'
            else:
                is_promoting = '未推广'
            res['data'].append({'id': i.id, 'device': i.device, 'account': i.account, 'status': online_status,
                                'sesstion_update_time': session_update_time, 'sequence': i.sequence,
                                'wechat_id': i.wechat_id, 'qq_id': i.qq_id, 'phone_number': i.phone_number,
                                'online_number': i.online_number, 'remark': i.remark, 'belong_to_whom': belong_to_whom,
                                'is_promoting': is_promoting, 'is_distributed': i.is_distributed,
                                'pid_list': i.pid_list})
    except Exception as e:
        res['code'] = 1
        res['message'] = e.__repr__()
    return res


def update_device_info(info):
    """
    更新账户设备信息
    :param info:
    :return: {'code': 0/1, 'message': error message, 'data': []}
    """
    res = {'code': 0, 'message': '', 'data': []}
    try:
        with transaction.atomic():  # 出错回滚
            if models.WebsiteDevice.objects.filter(device=info['device']).first():
                if info['is_promoting'] == '完成推广':
                    info['is_promoting'] = 0
                else:
                    info['is_promoting'] = 1
                models.WebsiteDevice.objects.filter(device=info['device']).update(device=info['device'],
                                                                                  account=info['account'],
                                                                                  wechat_id=info['wechat_id'],
                                                                                  qq_id=info['qq_id'],
                                                                                  sequence=info['sequence'],
                                                                                  phone_number=info['phone_number'],
                                                                                  online_number=info['online_number'],
                                                                                  remark=info['remark'],
                                                                                  is_promoting=info['is_promoting'],
                                                                                  pid_list=info['pid_list'],
                                                                                  )
            else:
                if info['is_promoting'] == '完成推广':
                    info['is_promoting'] = 0
                else:
                    info['is_promoting'] = 1
                models.WebsiteDevice.objects.create(**info)

    except Exception as e:
        res['code'] = 1
        res['message'] = e.__repr__()
    return res


def add_device():
    res = {'code': 1}
    return res


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
        if userinfo:
            if password == userinfo.password:
                # 登陆成功生成token保存并返回（以后每次请求都需携带这个token验证）
                token = create_token(username)
                models.WebsiteUserinfo.objects.filter(username=username).update(token=token)
                res['data']['token'] = token
                res['data']['role'] = userinfo.role  # 用户角色信息
                res['data']['uid'] = userinfo.id
                auth = {}.fromkeys([n.url for n in models.WebsiteAuth.objects.all()], False)  # 获取用户拥有的权限
                for i in userinfo.userauth.all():
                    auth[i.url] = True
                res['data']['auth'] = auth
                # #权限
                # res['data']['realtimeData'] = True
                # res['data']['adilyData'] = True

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


def get_record(start_time, end_time, method='payment_all'):
    """
    获取转账记录
    :param start_time: 开始时间
    :param end_time:  结束时间
    :param method: 记录类型（默认全部）

    :return: {'code':0/1, 'message': error message ,\
                'data':[{'amount':  ,'account':  ,'name':  ,'remark':  , 'out_biz_no':  ,'status':  }, {   },  {   } ]}
    """
    res = {'code': 0, 'message': "", 'data': []}
    first_pay_status_dict = {'first_succ': 1, 'no_first_succ': 0, }
    try:
        # 没有传递参数默认显示当天数据
        if not start_time or not end_time:
            end_time = datetime.datetime.now().strftime("%Y-%m-%d")
            start_time = end_time

        # 前端传递的时间格式为2018-08-08，由于数据库里面时通过order_id字段查询时间格式为20180808，需要处理时间格式
        # 因为要比较outbizno 后面增加10个0
        start_time = start_time.replace('-', '') + '0' * 10
        end_time = end_time.replace('-', '') + '9' * 10
        # 查询所有的转账记录
        if method == 'payment_all':
            info = models.WebsitePayment.objects.filter(out_biz_no__gte=start_time).filter(
                out_biz_no__lte=end_time).all()
        # 查询转账失败记录(已补交和未补缴)的记录
        elif method == 'payment_fail':
            info = models.WebsitePayment.objects.filter(out_biz_no__gte=start_time).filter(
                out_biz_no__lte=end_time, first_pay_status=first_pay_status_dict['no_first_succ']).all()
        # 待补交(未补缴)
        else:
            info = models.WebsitePayment.objects.filter(out_biz_no__gte=start_time).filter(
                out_biz_no__lte=end_time, first_pay_status=first_pay_status_dict['no_first_succ']).exclude(
                status='转账成功').all()

        for i in info:
            res['data'].append(
                {'amount': i.amount, 'account': i.payee_account, 'name': i.payee_real_name, 'remark': i.remark,
                 'out_biz_no': i.out_biz_no, 'status': i.status, 'first_pay_status': i.first_pay_status,
                 'pay_date': i.pay_date})

    except Exception as e:
        res['code'] = 1
        res['message'] = e.__repr__()

    return res


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

    def add_user(self, name, password, auth, real_name, group, sex='male', gid='1'):
        # 增加新用户

        role_dict = {"客服": "1", "管理员": "2", '股东': '4', '合伙人': '5', '主管': '6'}
        try:
            if models.WebsiteUserinfo.objects.filter(username=name):
                return False
            else:
                models.WebsiteUserinfo.objects.create(username=name, password=password, sex=sex, gid_id=gid,
                                                      role=role_dict[group], name=real_name).userauth.set(auth)
                if group == '股东' or group == '合伙人':
                    new_id = models.WebsiteUserinfo.objects.order_by('-id').first().id
                    models.WebsiteShareholderinfo.objects.create(sh_id_id=new_id)

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

    def update_user(self, id, name, password, auth, real_name, group, role=None):
        """
        更新用户信息
        :param id:用户id
        :param name:登录名
        :param password: 密码
        :param auth: 权限
        :param gid: 用户组id
        :param role: 用户类型
        :return: true/false
        """
        role_dict = {"客服": "1", "管理员": "2", '股东': '4', '合伙人': '5', '主管': '6'}
        try:
            data = models.WebsiteUserinfo.objects.filter(id=id)
            if data:
                data.update(password=password, name=real_name, role=role_dict[group])
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
    :return:{'code': 0/1, 'message': error message, 'data':[ {'device':  'account':  }, {  }, {  }]}
    """
    res = {'code': 0, 'message': '', 'data': []}
    role_dict = {"1": "客服", "2": "管理员", "3": "超级管理员", '4': '股东', '5': '合伙人', '6': '主管', }
    try:
        data = models.WebsiteUserinfo.objects.all()
        for i in data:
            # get all auth of user
            auth = {}.fromkeys([n.url for n in models.WebsiteAuth.objects.all()], False)  # 获取用户拥有的权限
            for j in i.userauth.all():
                auth[j.url] = True
            i.role = role_dict[i.role]
            res['data'].append(
                {'id': i.id, 'username': i.username, 'real_name': i.name, 'password': i.password, 'group': i.role,
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


def review_device_state(request_month):
    """
        查看设备状态
        :param request_month: 查看月份
        :return: {'code':0/1, 'message': error message ,\
                    'data':[{'device':  ,'account':  ,'payment':  ,'balance':  , 'effect':  ,'estimate':  ,'valod':\
                            'settlementOrders':  ,'goods':  },  {   },  {   } ]}
        """
    res = {'code': 0, 'message': "", 'data': []}
    try:
        query_set = models.WebsiteDeviceState.objects.filter(date__startswith=request_month).all()
        temp_name_dict = {}
        temp_name_list = []
        for item in list(models.WebsiteDevice.objects.values_list('device', 'id').order_by('sequence').all()):
            if item[0] == '代理' or item[0] == '朋友圈':
                continue
            temp_name_list.append(item[1])
            # 初始化数据
            temp_record = {'name': item[0],
                           'eid': item[1],
                           'data': {}
                           }
            res['data'].append(temp_record)
        for item in query_set:
            # item[0]:name ; [1]:item ; [2]:score ; [3]:date
            # 新姓名
            index_date = str(int(item.date[-2:]))
            if item.device_rawid_id not in temp_name_list:
                temp_name_list.append(item.device_rawid_id)
                # temp_name_dict[item.device_rawid_id] = item.device_rawid.device
                temp_record = {'name': item.device_rawid.device,
                               'eid': item.device_rawid_id,
                               'data': {'state_id' + index_date: item.id, 'i' + index_date: item.device_state}
                               }
                res['data'].append(temp_record)

            # 已经在记录中
            else:
                index_record = temp_name_list.index(item.device_rawid_id)
                res['data'][index_record]['data']['state_id' + index_date] = item.id
                res['data'][index_record]['data']['i' + index_date] = item.device_state
    except Exception as e:
        res['code'] = 1
        res['message'] = e.__repr__()
    return res


def update_device_state(edit_info):
    """
       更新设备状态
       :param edit_info: 设备信息
       info : {
            eid :  ‘设备id’,
            date : ’2018-11-04’,
            state : “.....”,
            remark : ‘.....’ ,}
       :return: {'code': 0/1, 'message': error message, 'data': []}
       """
    res = {'code': 0, 'message': '', 'data': []}
    # 通过是否传递了time来判断是修改还是新建
    try:
        with transaction.atomic():  # 出错回滚
            if edit_info:  # 修改
                # 判断修改还是新增
                if 'remark' not in edit_info.keys():
                    edit_info['remark'] = ''
                if models.WebsiteDeviceState.objects.filter(device_rawid=edit_info['eid'], date=edit_info['date']):
                    models.WebsiteDeviceState.objects.filter(device_rawid=edit_info['eid'],
                                                             date=edit_info['date']).update(
                        device_state=edit_info['state'],
                        remark=edit_info['remark'])
                    res['message'] = str(edit_info['eid']) + '的状态修改成功'
                else:
                    models.WebsiteDeviceState.objects.create(device_rawid_id=edit_info['eid'], date=edit_info['date'],
                                                             device_state=edit_info['state'],
                                                             remark=edit_info['remark'])
                    res['message'] = str(edit_info['eid']) + '的状态创建成功'
    except Exception as e:
        res['code'] = 1
        res['message'] = e.__repr__()
    return res


# def get_tran_record():
#     res = {'code': 0, 'message': '', 'data': []}
#     try:
#         a = models.WebsiteTranRecord.objects.filter(status=0).all()
#         b = serializers.serialize('json', a)
#         res['data'] = json.loads(b)
#     except Exception as e:
#         res['code'] = 1
#         res['message'] = e.__repr__()
#     print(res)
#     print(type(res))
#     return res
