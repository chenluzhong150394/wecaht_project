# import calendar
# import copy
#
# from website import models
# from django.db.models import Sum
# from django.db.models import Avg
# from django.db import transaction
# from utils.time_tools import time_list, day
# from datetime import datetime
# from dateutil.relativedelta import relativedelta
# import re
# import json
# import hashlib
# import time
# import datetime
# from django.db.models import Q
# from utils.payment_interface import Payment as Pay
# from django.db.models import Count
# from django.forms.models import model_to_dict
# import traceback
# from django.core import serializers
#
#
#
# class API(object):
#     """
#     所有用户信息获取接口
#     """
#
#     def __init__(self):
#         self.res = {'code': 0, 'message': '', 'data': {}}
#
#
#     def get_user_url(self, name):
#         """
#         获取用户的拥有的url
#         :param name: 用户名
#         :return: ['url','url'...] /false
#         """
#         data = models.WebsiteUserinfo.objects.filter(username=name).first()
#         res = []
#         if data:
#             for i in data.userauth.all():
#                 for u in re.split('[,， ]', i.url):
#                     res.append(u)
#             return res
#         else:
#             return False
#
#     def get_all_user_name(self):
#         """
#         获取用户的拥有的url
#         :param none
#         :return: ['root','admin'...] /false
#         """
#         data = models.WebsiteUserinfo.objects.values_list('username').distinct()
#         if data:
#             res = [i[0] for i in data]
#             return res
#         else:
#             return False
#
#     def get_user_aid(self, name):
#         """
#         获取用户权限id
#         :param name: 用户名
#         :return: '1234'/false
#         """
#         data = models.WebsiteUserinfo.objects.filter(username=name).first()
#         res = ""
#         if data:
#             for i in data.userauth.all():
#                 res += str(i.id)
#                 res += ','
#             self.res['data'] = res
#             return self.res
#         else:
#             return False
#
#     def get_user_gid(self, name):
#         """
#         获取用户的gid
#         :param name: 用户名
#         :return: gid/false
#         """
#         data = models.WebsiteUserinfo.objects.filter(username=name).first()
#         if data:
#             self.res['data'] = data.gid.gid
#             return self.res
#         else:
#             self.res['code'] = 1
#             return self.res
#
#
#     def get_auth_info(self):
#         """
#         获取所有权限信息
#         :return: [{'name': authname, 'id': authid, 'title': authtitle, 'url': authurl},........]
#         """
#         info = []
#         data = models.WebsiteAuth.objects.all()
#         for d in data:
#             info.append({'id': d.id, 'name': d.name, 'title': d.title, 'url': d.url})
#         return info
#
#
#     def remove_auth(self, name):
#         """
#         删除权限，所有用户的这个权限都会被删除
#         :param name: 权限名
#         :return: true/false
#         """
#         try:
#             models.WebsiteAuth.objects.filter(name=name).delete()
#             return True
#         except Exception as e:
#             print(e)
#             return False
#
#     def add_user(self, name, password, auth, real_name, role, sex='male'):
#         # 增加新用户
#
#         role_dict = {"管理员": "1", "客服": "2"}
#         try:
#             if models.WebsiteUserinfo.objects.filter(username=name):
#                 return False
#             else:
#                 models.WebsiteUserinfo.objects.create(username=name, password=password, sex=sex,
#                                                       role=role_dict[role], name=real_name).userauth.set(auth)
#                 return True
#
#         except Exception as e:
#             print(e)
#             return False
#
#     def remove_user(self, id):
#         # 删除用户
#         try:
#             models.WebsiteUserinfo.objects.filter(id=id).delete()
#             return True
#         except Exception as e:
#             return False
#
#     def update_user(self, id, username, password, auth, real_name, role):
#         """
#         更新用户信息
#         :param id:用户id
#         :param username:登录名
#         :param password: 密码
#         :param auth: 权限
#         :param real_name: 姓名
#         :param role: 用户类型
#         :return: true/false
#         """
#         role_dict = {"管理员": "1", "客服": "2"}
#         try:
#             data = models.WebsiteUserinfo.objects.filter(id=id)
#             if data:
#                 data.update(password=password, username=username, name=real_name, role=role_dict[role])
#                 data.first().userauth.set(auth)
#                 return True
#             else:
#                 return False
#
#         except Exception as e:
#             return False
#
#     def update_auth(self, name, url):
#         """
#         更新或新建权限
#         :param name: 标题
#         :param url: 链接地址
#         :return: true/false
#         """
#         try:
#             data = models.WebsiteAuth.objects.filter(name=name)
#             if data:
#                 data.update(url=url)
#             else:
#                 models.WebsiteAuth.objects.create(name=name, url=url)
#             return True
#
#         except Exception as e:
#             print(e)
#             return False