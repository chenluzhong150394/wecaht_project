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
    role = models.IntegerField(null=True, default=0) # 用户的角色 -- 默认0是管理员

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

# 关注者的信息模型
class user_openID(models.Model):
    user = models.CharField(max_length=32, blank=True, null=True)  # 微信名
    openID = models.CharField(max_length=128,blank=True,null=True)  #openid
    remark = models.CharField(max_length=128,blank=True,null=True)  # 备注信息
    subscribe_time = models.CharField(max_length=36,blank=True,null=True)  # 关注时间
    position = models.CharField(max_length=36,blank=True,null=True) # 国家
    city = models.CharField(max_length=36,blank=True,null=True)     # 城市
    headimgurl = models.CharField(max_length=256,blank=True,null=True)     # 头像地址
    subscribe = models.IntegerField(default=1)     # 是否关注
    class Mata:
        managed = True
        db_table = 'weixin_userlist'
