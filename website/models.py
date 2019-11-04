# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
import django.utils.timezone as timezone


class WebsiteDevice(models.Model):
    account = models.CharField(max_length=64, blank=True, null=True)
    device = models.CharField(unique=True, max_length=64, blank=True, null=True)
    ad_id = models.CharField(max_length=300, blank=True, null=True)
    wechat_id = models.CharField(max_length=20, blank=True, null=True)
    qq_id = models.CharField(max_length=20, blank=True, null=True)
    phone_number = models.CharField(max_length=13, blank=True, null=True)
    online_number = models.CharField(max_length=13, blank=True, null=True)
    remark = models.TextField(blank=True, null=True)
    sequence = models.IntegerField(blank=True, null=True)
    session_key = models.CharField(max_length=100, blank=True, null=True)
    is_distributed = models.IntegerField(blank=True, null=True)
    is_promoting = models.IntegerField(blank=True, null=True)
    pid_list = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'website_device'


class WebsiteDownloadLog(models.Model):
    uid = models.IntegerField()
    user_name = models.CharField(max_length=255)
    type = models.CharField(max_length=255)
    start_time = models.CharField(max_length=255)
    end_time = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'website_download_log'



class WebsitePayment(models.Model):
    id = models.AutoField(primary_key=True)
    payee_account = models.CharField(max_length=64, blank=True, null=True)
    amount = models.CharField(max_length=64, blank=True, null=True)
    payee_real_name = models.CharField(max_length=64, blank=True, null=True)
    remark = models.CharField(max_length=64, blank=True, null=True)
    order_id = models.CharField(max_length=64, blank=True, null=True)
    out_biz_no = models.CharField(max_length=64, blank=True, null=True)
    pay_date = models.CharField(max_length=64, blank=True, null=True)
    status = models.CharField(max_length=64, blank=True, null=True)
    first_pay_status = models.IntegerField(blank=True, null=True)
    success_time = models.CharField(max_length=40, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'website_payment'


class WebsiteAuth(models.Model):
    name = models.CharField(max_length=255, unique=True)
    title = models.CharField(max_length=255, null=True)
    url = models.CharField(max_length=255, null=True)

    class Meta:
        managed = False
        db_table = 'website_auth'




class WebsiteUserinfo(models.Model):
    uid = models.IntegerField(unique=True)
    name = models.CharField(max_length=255, null=True)
    username = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=64)
    sex = models.CharField(max_length=16, null=True)
    birthday = models.CharField(max_length=64, null=True)
    tel = models.CharField(max_length=64, null=True)
    email = models.CharField(max_length=64, null=True)
    address = models.CharField(max_length=64, null=True)
    introduction = models.CharField(max_length=255, null=True)
    role = models.CharField(max_length=32, null=True)
    auth_type = models.CharField(max_length=32, null=False, default='默认')
    userauth = models.ManyToManyField(WebsiteAuth)
    token = models.CharField(max_length=255)
    is_distributed = models.IntegerField

    class Meta:
        managed = False
        db_table = 'website_userinfo'



class WebsiteLog(models.Model):
    username = models.CharField(max_length=255)
    record = models.CharField(max_length=255)
    time = models.DateTimeField(default=timezone.now)

    class Meta:
        managed = False
        db_table = 'website_log'


class WebsiteBalanceRecord(models.Model):
    account_name = models.CharField(max_length=25, blank=True, null=True)
    balance = models.FloatField(blank=True, null=True)
    update_time = models.CharField(max_length=20, blank=True, null=True)
    last_time_balance = models.FloatField(blank=True, null=True)
    last_cost = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'website_balance_record'


"""
新增功能
"""


# 转账 账单信息
class WebsiteTranRecord(models.Model):
    # 金额
    money = models.FloatField(blank=True, null=True)
    # 姓名
    name = models.CharField(max_length=30, blank=True, null=True)
    # 账号
    zfb_number = models.CharField(max_length=30, blank=True, null=True)
    # 设备号
    device = models.CharField(max_length=64, blank=True, null=True)
    # 转账时间
    pay_date = models.CharField(max_length=64, blank=True, null=True)
    # 交易号
    order_id = models.CharField(max_length=64, blank=True, null=True)
    # 交易备注（失败的原因）
    remark = models.CharField(max_length=64,blank=True,null=True)
    # 后端生成的一个编号（时间+随机数）
    out_biz_no = models.CharField(max_length=64, blank=True, null=True)
    # 状态(0是待转账，1是成功，2是失败，3是再次转账成功)
    status = models.IntegerField(null=True, default=0)
    # 操作人
    operator = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        db_table = 'website_tran_record'


# 设备信息表
class Device_Information(models.Model):
    # 服务器
    server = models.CharField(max_length=32, blank=True, null=True)
    # 设备号
    device = models.CharField(max_length=32, blank=True, null=True)
    # 软件账号
    software_account = models.CharField(max_length=32, blank=True, null=True)
    # 软件密码
    software_password = models.CharField(max_length=32, blank=True, null=True)
    # 微信账号
    wechat_id = models.CharField(max_length=32, blank=True, null=True)
    # 软件运行情况
    software_status = models.IntegerField(null=True, default=0)
    # 微信在线情况
    wechat_status = models.IntegerField(null=True, default=0)
    # 检测时间
    test_time = models.CharField(max_length=30, blank=True, null=True)
    # 备注信息
    remarks_information = models.CharField(max_length=32, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'device_information'


# 余额表
class Balance_Information(models.Model):
    balance = models.FloatField(blank=True, null=True)
    time = models.CharField(max_length=30, blank=True, null=True)
    status = models.IntegerField(null=True, default=0)
    balance_change = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'balance_information'
