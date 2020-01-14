# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
import django.utils.timezone as timezone



class Token(models.Model):
    token = models.CharField(max_length=512, blank=True, null=True)  # token

    class Mata:
        managed = True
        db_table = 'token'


class Userinfo(models.Model):
    user = models.CharField(max_length=64, blank=True, unique=True)  # 用户名
    passwd = models.CharField(max_length=64, blank=True, null=True)  # 密码
    remark = models.CharField(max_length=64,blank=True, null=True)  # 备注
    real_name = models.CharField(max_length=64,blank=True, null=True)  # 真实姓名
    create_time = models.CharField(max_length=64,blank=True, null=True)  # 用户注册时间
    update_time = models.CharField(max_length=64,blank=True, null=True)  # 最近一次更改时间

    class Mata:
        managed = True
        db_table = 'Userinfo'


class envent(models.Model):
    userID = models.CharField(max_length = 64,default=None)
    eventID = models.CharField(max_length = 64,default=None)
    remark = models.CharField(max_length=339,blank=True,null=True)
    class Mata:
        managed = True
        db_table = 'weixin_envent'

class user_openID(models.Model):
    user = models.CharField(max_length=32, blank=True, null=True)  # 记录ID
    openID = models.CharField(max_length=128,blank=True,null=True)
    remark = models.CharField(max_length=128,blank=True,null=True)
    class Mata:
        managed = True
        db_table = 'weixin_userlist'
