from django.conf.urls import url
from website import views
urlpatterns = [
    url(r'^login$', views.Login.as_view()),  # 登陆验证 1


    #账目
    url(r'^money$', views.payment.as_view()),  # 转账接口（websocket链接开始转账）
    url(r'^moneylog1$', views.PaymentRecord.as_view()),  # 获取转账记录
    url(r'^download_log$', views.download_log),  # 记录下载log
    url(r'^exec_each_machines$', views.get_excel),  # 激活下载器
    url(r'^upload_excel$', views.upload_excel),  # 上传转账表
    url(r'^download_transfer_excel$', views.download_excel),   # 下载转账表

    #余额
    url(r'^balance_preview$', views.balance_preview),  # 余额查看 1
    url(r'^balance_deposit$', views.balance_deposit),  # 存钱增加余额 1

    #权限
    url(r'^manage$', views.Manager_review.as_view()),   # 用户管理 /查看权限1
    url(r'^edituser$', views.Manager_user_auth.as_view()),   # 添加用户 /新增用户1
    url(r'^update_user_info$', views.Update_person_info.as_view()),   # 修改权限 /修改某人权限1
    url(r'^remove_user$', views.Remove_user.as_view()),   # 删除用户 1
    url(r'^change_password$', views.change_password),   # 修改密码 1
    url(r'^get_userinfo', views.get_userinfo),   # 个人中心 获取当前登录账户的信息 1



    #操作日志
    url(r'^operationlog$', views.Operationlog.as_view()),   # 查看操作日志 1

    # 设置支付宝api接口配置信息
    url(r'update_settings$', views.update_pay_ses),  # 添加支付宝配置信息 1
    url(r'read_settings$', views.Read_pay_key),  # 查看支付宝配置信息 1

    # 转账信息
    url(r'^tranrecord$', views.Get_tran_record.as_view()),  # 获取今日提现信息 1
    url(r'^tranrecord1$', views.Get_tran_record1.as_view()),  # 获取转账记录信息 1
    url(r'^tranrecord2$', views.Get_tran_record2.as_view()),  # 获取待处理提现 1
    url(r'^uptranrecord$', views.Updata_tran_record.as_view()),  # 待处理提现信息修改接口 1
    url(r'^tranmonery$', views.Get_tran_monery.as_view()),  # 获取主页转账笔数金额 1

    # 主页获取设备状态
    url(r'^devicestatus$', views.get_device_information),  # 主页设备状态获取 1
    url(r'^get_devicestatus$', views.run_device_state),  # 调用远程服务器脚本获取设备信息 1


    # 写入数据库设备状态
    url(r'^writedevicestatus$', views.write_device_information),  # 写入数据库设备状态 1
]
