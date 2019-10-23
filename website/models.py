# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
import django.utils.timezone as timezone

class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    # user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class MonetCountAmountCreateTime(models.Model):
    user_name = models.CharField(primary_key=True, max_length=255)
    day_time = models.CharField(max_length=10)
    count = models.IntegerField(blank=True, null=True)
    device_name = models.CharField(max_length=255)
    class Meta:
        managed = False
        db_table = 'monet_count_amount_create_time'
        unique_together = (('user_name', 'day_time'),)


class MoneyAmount(models.Model):
    user_name = models.CharField(primary_key=True, max_length=255)
    day_time = models.CharField(max_length=10)
    count = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    device_name =  models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'money_amount'
        unique_together = (('user_name', 'day_time'),)


class MoneyCountAmountSettlement(models.Model):
    user_name = models.CharField(primary_key=True, max_length=255)
    day_time = models.CharField(max_length=10)
    count = models.IntegerField(blank=True, null=True)
    device_name = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'money_count_amount_settlement'
        unique_together = (('user_name', 'day_time'),)


class MoneyEstEffectCreateTime(models.Model):
    user_name = models.CharField(primary_key=True, max_length=255)
    day_time = models.CharField(max_length=10)
    count = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    device_name = models.CharField(max_length=255)
    class Meta:
        managed = False
        db_table = 'money_est_effect_create_time'
        unique_together = (('user_name', 'day_time'),)


class MoneyEstEffectSettlementTime(models.Model):
    user_name = models.CharField(primary_key=True, max_length=255)
    day_time = models.CharField(max_length=10)
    count = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    device_name = models.CharField(max_length=255)
    class Meta:
        managed = False
        db_table = 'money_est_effect_settlement_time'
        unique_together = (('user_name', 'day_time'),)


class MoneySettlement(models.Model):
    user_name = models.CharField(primary_key=True, max_length=255)
    day_time = models.CharField(max_length=10)
    count = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    device_name = models.CharField(max_length=255)
    class Meta:
        managed = False
        db_table = 'money_settlement'
        unique_together = (('user_name', 'day_time'),)


class Oa(models.Model):
    user_name = models.CharField(max_length=255)
    create_time = models.CharField(max_length=32, blank=True, null=True)
    click_time = models.CharField(max_length=32)
    goods_info = models.CharField(max_length=128, blank=True, null=True)
    goods_id = models.CharField(max_length=32)
    wangwang = models.CharField(max_length=64, blank=True, null=True)
    shop_name = models.CharField(max_length=64, blank=True, null=True)
    goods_num = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    goods_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    order_status = models.CharField(max_length=32, blank=True, null=True)
    order_type = models.CharField(max_length=32, blank=True, null=True)
    income_ratio = models.CharField(max_length=32, blank=True, null=True)
    division = models.CharField(max_length=32, blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    est_effect = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    settlement = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    est_income = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    settlement_time = models.CharField(max_length=32, blank=True, null=True)
    com_ratio = models.CharField(max_length=32, blank=True, null=True)
    com_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    service = models.CharField(max_length=32, blank=True, null=True)
    sub_ratio = models.CharField(max_length=32, blank=True, null=True)
    sub_price = models.CharField(max_length=32, blank=True, null=True)
    sub_type = models.CharField(max_length=32, blank=True, null=True)
    platform = models.CharField(max_length=32, blank=True, null=True)
    third_server = models.CharField(max_length=64, blank=True, null=True)
    order_num = models.CharField(max_length=32)
    type = models.CharField(max_length=32, blank=True, null=True)
    source_id = models.CharField(max_length=32)
    source_name = models.CharField(max_length=32, blank=True, null=True)
    ad_id = models.CharField(max_length=32)
    ad_name = models.CharField(max_length=32, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'oa'
        unique_together = (('goods_id', 'order_num'),)
        ordering = ['-create_time']


class OaReflection(models.Model):
    user_name = models.CharField(max_length=255)
    create_time = models.CharField(max_length=32, blank=True, null=True)
    click_time = models.CharField(max_length=32)
    goods_info = models.CharField(max_length=128, blank=True, null=True)
    goods_id = models.CharField(max_length=32)
    wangwang = models.CharField(max_length=64, blank=True, null=True)
    shop_name = models.CharField(max_length=64, blank=True, null=True)
    goods_num = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    goods_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    order_status = models.CharField(max_length=32, blank=True, null=True)
    order_type = models.CharField(max_length=32, blank=True, null=True)
    income_ratio = models.CharField(max_length=32, blank=True, null=True)
    division = models.CharField(max_length=32, blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    est_effect = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    settlement = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    est_income = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    settlement_time = models.CharField(max_length=32, blank=True, null=True)
    com_ratio = models.CharField(max_length=32, blank=True, null=True)
    com_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    service = models.CharField(max_length=32, blank=True, null=True)
    sub_ratio = models.CharField(max_length=32, blank=True, null=True)
    sub_price = models.CharField(max_length=32, blank=True, null=True)
    sub_type = models.CharField(max_length=32, blank=True, null=True)
    platform = models.CharField(max_length=32, blank=True, null=True)
    third_server = models.CharField(max_length=64, blank=True, null=True)
    order_num = models.CharField(max_length=32)
    type = models.CharField(max_length=32, blank=True, null=True)
    source_id = models.CharField(max_length=32)
    source_name = models.CharField(max_length=32, blank=True, null=True)
    ad_id = models.CharField(max_length=32)
    ad_name = models.CharField(max_length=32, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'oa_reflection'


class OnlineStatua(models.Model):
    user_id = models.CharField(primary_key=True, max_length=20)
    end_time = models.CharField(max_length=20)
    statua = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'online_statua'
        unique_together = (('user_id', 'end_time', 'statua'),)

class OutputFromCibuluo(models.Model):
    device_name = models.CharField(primary_key=True, max_length=255)
    date_time = models.CharField(max_length=20)
    total_customer = models.IntegerField(blank=True, null=True)
    device_customer = models.IntegerField(blank=True, null=True)
    total_count = models.FloatField(blank=True, null=True)
    output_from_cibuluo = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'output_from_cibuluo'
        unique_together = (('device_name', 'date_time'),)


class SumGoods(models.Model):
    user_name = models.CharField(primary_key=True, max_length=255)
    day_time = models.CharField(max_length=10)
    sum_goods = models.IntegerField(blank=True, null=True)
    device_name = models.CharField(max_length=255)
    class Meta:
        managed = False
        db_table = 'sum_goods'
        unique_together = (('user_name', 'day_time'),)

class WebsiteAccountRealOutputRecord(models.Model):
    account_name = models.TextField(blank=True, null=True)
    request_month = models.CharField(max_length=255, blank=True, null=True)
    real_output = models.FloatField(blank=True, null=True)

    record_source = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'website_account_real_output_record'

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
    belong_group = models.ForeignKey('WebsiteGroup', models.DO_NOTHING, db_column='belong_group', blank=True, null=True)
    ad_id_list = models.CharField(max_length=300, blank=True, null=True)
    pid_list = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'website_device'



class MoneyOrderRatio(models.Model):
    user_name = models.CharField(primary_key=True, max_length=255)
    day_time = models.CharField(max_length=10)
    sum_goods = models.IntegerField(blank=True, null=True)
    order_ratio = models.FloatField(blank=True, null=True)
    device = models.CharField(max_length=255, blank=True, null=True)
    data = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'money_order_ratio'
        unique_together = (('user_name', 'day_time'),)


class WebsiteDownloadLog(models.Model):
    uid = models.IntegerField()
    user_name = models.CharField(max_length=255)
    type = models.CharField(max_length=255)
    start_time = models.CharField(max_length=255)
    end_time = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'website_download_log'

class WebsiteInputdata(models.Model):
    uid = models.AutoField(primary_key=True)
    username = models.CharField(max_length=64, blank=True, null=True)
    time = models.CharField(max_length=64, blank=True, null=True)
    data = models.CharField(max_length=64, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'website_inputdata'
        # ordering = ['-time']


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


class WebsiteGroup(models.Model):
    groupname = models.CharField(unique=True, max_length=255)

    class Meta:
        managed = False
        db_table = 'website_group'


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
    gid = models.ForeignKey(WebsiteGroup, models.DO_NOTHING, null=True)
    auth_type = models.CharField(max_length=32, null=False, default='默认')
    userauth = models.ManyToManyField(WebsiteAuth)
    token = models.CharField(max_length=255)
    is_distributed = models.IntegerField

    class Meta:
        managed = False
        db_table = 'website_userinfo'


class WebsiteDeviceReserve(models.Model):
    device = models.ForeignKey(WebsiteDevice, models.DO_NOTHING, blank=True, null=True)
    month = models.CharField(max_length=255, blank=True, null=True)
    reserve = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'website_device_reserve'

class WebsitePartnerRecord(models.Model):
    month = models.CharField(max_length=20, blank=True, null=True)
    partner_single_profit1 = models.FloatField(blank=True, null=True)
    partner_single_profit2 = models.FloatField(blank=True, null=True)
    partner = models.CharField(max_length=255, blank=True, null=True)
    partner_0 = models.ForeignKey('WebsiteShareholderinfo', models.DO_NOTHING, db_column='partner_id', blank=True, null=True)  # Field renamed because of name conflict.
    partner_ratio = models.FloatField(blank=True, null=True)
    partner_own_device_num = models.IntegerField(blank=True, null=True)
    partner_profit = models.FloatField(blank=True, null=True)
    single_profit_avg = models.FloatField(blank=True, null=True)
    partner_single_cost = models.FloatField(blank=True, null=True)
    month_single_profit = models.FloatField(blank=True, null=True)
    partner_customer_avg = models.FloatField(blank=True, null=True)
    partner_single_cibuluo = models.FloatField(blank=True, null=True)
    partner_single_profit = models.FloatField(blank=True, null=True)
    single_device_output = models.FloatField(blank=True, null=True)
    single_device_cost = models.FloatField(blank=True, null=True)
    single_device_profit = models.FloatField(blank=True, null=True)
    partner_device_profit = models.FloatField(blank=True, null=True)
    single_device_output_avg = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'website_partner_record'



class WebsiteDeviceMonthProfit(models.Model):
    device_name = models.CharField(max_length=10)
    device = models.ForeignKey(WebsiteDevice, models.DO_NOTHING)
    belong_to_whom = models.CharField(max_length=10, blank=True, null=True)
    belong_to_whom_id = models.IntegerField(blank=True, null=True)
    belong_to_whom_ratio = models.FloatField(blank=True, null=True)
    account_name = models.CharField(max_length=30, blank=True, null=True)
    request_month = models.CharField(max_length=15, blank=True, null=True)
    output = models.FloatField(blank=True, null=True)
    output_from_cibuluo = models.FloatField(blank=True, null=True)
    cost_payment = models.FloatField(blank=True, null=True)
    real_output_from_cibuluo = models.FloatField(blank=True, null=True)
    avg_device_customer = models.FloatField(blank=True, null=True)
    avg_all_device_customer = models.FloatField(blank=True, null=True)
    cost_rent_base_device = models.FloatField(blank=True, null=True)
    cost_man_power_base_device = models.FloatField(blank=True, null=True)
    cost_device_base_device = models.FloatField(blank=True, null=True)
    raw_device_profit_base_device = models.FloatField(blank=True, null=True)
    profit_base_device = models.FloatField(blank=True, null=True)
    avg_profit = models.FloatField(blank=True, null=True)
    this_month_reserve = models.FloatField(blank=True, null=True)
    cost_reserve = models.FloatField(blank=True, null=True)
    cost_rent_base_customer = models.FloatField(blank=True, null=True)
    cost_man_power_base_customer = models.FloatField(blank=True, null=True)
    cost_device_base_customer = models.FloatField(blank=True, null=True)
    raw_device_profit_base_customer = models.FloatField(blank=True, null=True)
    raw_profit_sum_base_customer = models.FloatField(blank=True, null=True)
    profit_base_customer = models.FloatField(blank=True, null=True)
    last_month_reserve = models.FloatField(blank=True, null=True)
    raw_profit_base_device = models.FloatField(blank=True, null=True, default=0.0)
    raw_profit_base_customer = models.FloatField(blank=True, null=True, default=0.0)
    class Meta:
        managed = False
        db_table = 'website_device_month_profit'

class WebsiteAccountOutputRecord(models.Model):
    account_name = models.TextField(blank=True, null=True)
    request_month = models.CharField(max_length=255, blank=True, null=True)
    real_output = models.FloatField(blank=True, null=True)
    device_name = models.CharField(max_length=100, blank=True, null=True , default='')
    raw_output = models.FloatField(blank=True, null=True , default=0.0)
    output_from_cibuluo = models.FloatField(blank=True, null=True, default=0.0)
    cost_payment = models.FloatField(blank=True, null=True, default=0.0)
    belong_to_whom = models.CharField(max_length=10, blank=True, null=True)
    belong_to_whom_id = models.IntegerField(blank=True, null=True, default=0)
    belong_to_whom_ratio = models.FloatField(blank=True, null=True, default=0.0)
    real_output_from_cibuluo = models.FloatField(blank=True, null=True, default=0.0)
    cost_reserve = models.FloatField(blank=True, null=True, default=0.0)
    this_month_reserve = models.FloatField(blank=True, null=True, default=0.0)
    last_month_reserve = models.FloatField(blank=True, null=True, default=0.0)
    cost_rent_base_customer = models.FloatField(blank=True, null=True, default=0.0)
    cost_man_power_base_customer = models.FloatField(blank=True, null=True, default=0.0)
    cost_device_base_customer = models.FloatField(blank=True, null=True, default=0.0)
    raw_device_profit_base_customer = models.FloatField(blank=True, null=True, default=0.0)
    raw_profit_base_customer = models.FloatField(blank=True, null=True, default=0.0)
    profit_base_customer = models.FloatField(blank=True, null=True, default=0.0)
    remark = models.TextField(blank=True, null=True , default='')
    is_updated = models.IntegerField(blank=True, null=True, default=0)
    cost_rent_base_device = models.FloatField(blank=True, null=True, default=0.0)
    cost_man_power_base_device = models.FloatField(blank=True, null=True, default=0.0)
    cost_device_base_device = models.FloatField(blank=True, null=True, default=0.0)
    raw_device_profit_base_device = models.FloatField(blank=True, null=True, default=0.0)
    raw_profit_base_device = models.FloatField(blank=True, null=True, default=0.0)
    profit_base_device = models.FloatField(blank=True, null=True, default=0.0)
    avg_profit = models.FloatField(blank=True, null=True, default=0.0)
    record_source = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'website_account_output_record'



class WebsiteMonthCost(models.Model):
    id = models.IntegerField(primary_key=True)
    month = models.CharField(max_length=255, blank=True, null=True)
    employee_wages = models.FloatField(blank=True, null=True)
    rent = models.FloatField(blank=True, null=True)
    device_cost = models.FloatField(blank=True, null=True)
    cost_all = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'website_month_cost'


class WebsiteMonthProfitRecord(models.Model):
    id = models.IntegerField(primary_key=True)
    month = models.CharField(max_length=255, blank=True, null=True)
    account = models.CharField(max_length=255, blank=True, null=True)
    profit = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'website_month_profit_record'

class WebsiteShAlreadyReserveRecord(models.Model):
    edit_time = models.CharField(max_length=255, blank=True, null=True)
    sh = models.ForeignKey('WebsiteShareholderinfo', models.DO_NOTHING)
    real_reserve = models.FloatField(blank=True, null=True)
    remark = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'website_sh_already_reserve_record'


class WebsiteShReserveRecord(models.Model):
    month = models.CharField(max_length=255, blank=True, null=True)
    sh = models.ForeignKey('WebsiteShareholderinfo',  models.DO_NOTHING)
    logic_reserve = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'website_sh_reserve_record'



class WebsiteShareholderinfo(models.Model):
    need_storage = models.FloatField()
    already_storage = models.FloatField()
    sh_id = models.ForeignKey('WebsiteUserinfo', models.DO_NOTHING, db_column='SH_id_id')  # Field name made lowercase.
    sh_percent = models.FloatField(db_column='SH_percent', blank=True, null=True)  # Field name made lowercase.
    own_devices = models.ManyToManyField(WebsiteDevice)
    device_num = models.IntegerField()
    class Meta:
        managed = False
        db_table = 'website_shareholderinfo'


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

class websiteDeviceSession(models.Model):
    device_name = models.CharField(max_length=20,primary_key=True)
    datetime = models.CharField(max_length=30,blank=True, null=True)
    session_key = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'device_session'

class WebsiteStaffAchievement(models.Model):
    name = models.CharField(max_length=30, blank=True, null=True)
    date = models.CharField(max_length=20, blank=True, null=True)
    item = models.CharField(max_length=100, blank=True, null=True)
    score = models.FloatField(blank=True, null=True)
    note = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'website_staff_achievement'

class WebsitePaymentRecord(models.Model):
    device = models.CharField(primary_key=True, max_length=50)
    date_time = models.CharField(max_length=20)
    payment_sum = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'website_payment_record'
        unique_together = (('device', 'date_time'),)


class WebsiteDeviceState(models.Model):
    device_rawid = models.ForeignKey(WebsiteDevice, models.DO_NOTHING, db_column='device_rawid', blank=True, null=True)
    device_state = models.CharField(max_length=20, blank=True, null=True)
    remark = models.TextField(blank=True, null=True)
    date = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'website_device_state'

#
# class Order_Ratio(models.Model):
#     username = models.CharField(max_length=255)
#     record = models.CharField(max_length=255)
#     time = models.DateTimeField(default=timezone.now)
#
#     class Meta:
#         managed = False
#         db_table = 'website_log'
