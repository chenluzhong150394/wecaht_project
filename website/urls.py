from django.conf.urls import url
from website import views
urlpatterns = [
    url(r'^login$', views.Login.as_view()),  # 登陆验证


    #账目
    url(r'^money$', views.payment.as_view()),  # 转账接口（websocket链接开始转账）
    url(r'^moneylog1$', views.PaymentRecord.as_view()),  # 获取转账记录
    url(r'^download_log$', views.download_log),  # 记录下载log
    url(r'^exec_each_machines$', views.get_excel),  # 激活下载器
    url(r'^upload_excel$', views.upload_excel),  # 上传转账表
    url(r'^download_transfer_excel$', views.download_excel),   # 下载转账表

    #余额
    url(r'^balance_preview$', views.balance_preview),  # 余额查看
    url(r'^balance_deposit$', views.balance_deposit),  # 存钱增加余额

    #权限
    url(r'^manage$', views.Manager_review.as_view()),   # 查看权限
    url(r'^manage/edituser$', views.Manager_user_auth.as_view()),   # 新增权限
    url(r'^manage/update_user_info$', views.Update_person_info.as_view()),   # 修改某人权限
    url(r'^manage/remove_user$', views.Remove_user.as_view()),   # 删除某人权限
    url(r'^manage/change_password$', views.change_password),   # 修改密码
    url(r'^manage/get_userinfo', views.get_userinfo),   # 获取某个账户的信息

    # 股东
    url(r'^owndevices$', views.Preview_SH_own_devices),  # 查看设备
    url(r'^holder/adddevice$', views.Add_device),  # 增加设备
    url(r'^holder/deldevice$', views.Del_device),  # 删除设备
    url(r'^holder/add_cost$', views.add_cost),  # 增加/修改# 成本



    # 设置支付宝api接口配置信息
    url(r'update_setings$', views.update_pay_ses),  # 添加支付宝配置信息
    url(r'read_setings$',views.Read_pay_key),   # 查看支付宝配置信息



    #设备信息
    url(r'^devices1$', views.Device_review.as_view()),  # 查看设备信息
    url(r'^devices2$', views.Device_edit),  # 更新设备信息
    url(r'^devices2_add$', views.Device_edit),  # 添加设备信息
    url(r'^devices1/get_accouts$', views.get_accounts),  # 获取所有设备账号
    url(r'^devices1/get_devices$', views.get_all_devices),  # 获取所有设备号

    #设备状态
    url(r'^devicestate$', views.get_device_state.as_view()),  # 设备状态获取
    url(r'^set_device_state$', views.set_device_state),  # 更新设备状态




    #操作日志
    url(r'^operationlog$', views.Operationlog.as_view()),   # 查看操作日志

    # 获取转账信息
    url(r'^tranrecord$', views.get_tran_record),  # 获取未转账信息
    url(r'^tranrecord1$', views.get_tran_record1),  # 获取转账成功信息
    url(r'^tranrecord2$', views.get_tran_record2),  # 获取转账失败信息
    url(r'^tranrecord3$', views.get_tran_record3),  # 获取失败以后再次转账成功信息

    url(r'^tranmonery$', views.get_tran_monery),  # 获取转账笔数金额等相关信息

    # 获取设备状态
    url(r'^devicestatus$', views.get_device_information),  # 设备状态获取

    # 写入数据库设备状态
    url(r'^writedevicestatus$', views.write_device_information),  # 写入数据库设备状态
]
