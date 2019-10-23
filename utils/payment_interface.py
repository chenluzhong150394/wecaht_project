
from utils.read_excel import read_excel
#from utils.pay_record import write
from datetime import datetime
from alipay import AliPay
from website import models
import os
import random

current_path = os.path.dirname(__file__)


class Payment(object):
    def __init__(self, url="https://openapi.alipay.com/gateway.do"):
        '''
        支付接口初始化
        :param appid: 商户appid
        :param url: 支付宝接口url
        '''
        self.app_private_key_string = open(current_path + "/app_private_key.txt").read()  # 应用私钥（默认从两个TXT文件中读取）
        self.alipay_public_key_string = open(current_path + "/alipay_public_key.txt").read()  # 支付宝公钥
        self.appid = open(current_path + "/appid.txt").read()  # 支付宝应用id
        self.alipay_each = AliPay(
            appid=self.appid,
            app_notify_url=url,
            app_private_key_string=self.app_private_key_string,
            alipay_public_key_string=self.alipay_public_key_string,
            sign_type="RSA2",
            debug=False
        )

    def pay(self, payee_account, amount, payee_real_name=None, remark=None, payer_show_name=None,
            payee_type="ALIPAY_LOGONID"):
        '''
        发起转账
        :param payee_account: 收款方账户
        :param amount: 转账金额
        :param payee_real_name:收款方姓名
        :param remark: 转账备注
        :param payer_show_name: 付款方姓名
        :param payee_type: 收款方类型
        :return:
        '''
        out_biz_no = datetime.now().strftime("%Y%m%d%H%M%S") + str(random.randint(1000, 9999))
        data = {'payee_account': None, 'amount': None, 'payee_real_name': None, 'remark': None, 'order_id': None,
                'out_biz_no': None, 'pay_date': None, 'status': None}
        try:
            result = self.alipay_each.api_alipay_fund_trans_toaccount_transfer(
                out_biz_no=out_biz_no,
                payee_type=payee_type,  # 收款方账户类型
                payee_account=payee_account,  # 收款方账户
                amount=amount,  # 转账金额
                payee_real_name=payee_real_name,  # 收款方姓名（可选，若不匹配则转账失败）
                remark=remark,  # 转账备注
                payer_show_name=payer_show_name  # 付款方姓名

            )
        except:
            data['payee_account'] = payee_account
            data['amount'] = amount
            data['payee_real_name'] = payee_real_name
            data['status'] = "转账过程中超过支付宝限制时间，请排除已转账的记录重新转账！"
            # error = [payee_account, amount, payee_real_name, result['sub_msg'], result['out_biz_no']]
            return data
        # result={'code':'10000','msg':'Success','order_id': '','out_biz_no': '',  'pay_date': '2017-06-26 14:36:25'}
        # 接口文档：https://docs.open.alipay.com/api_28/alipay.fund.trans.toaccount.transfer

        try:
            if result['code'] == '10000':
                # if result['msg'] == "Success":
                #     print(payee_account + "  转账成功" + "  交易单号：" + result["out_biz_no"])
                data['payee_account'] = payee_account
                data['amount'] = amount
                data['payee_real_name'] = payee_real_name
                data['order_id'] = result['order_id']
                data['out_biz_no'] = result['out_biz_no']
                data['pay_date'] = result['pay_date']
                data['status'] = '转账成功'
                return data
            # 转账失败
            # result={'code': '40004', 'msg': 'Business Failed', 'sub_code': 'PAYEE_USER_INFO_ERROR', 'sub_msg': '支付宝账号和姓名不匹配，请确认姓名是否正确', 'out_biz_no': '20180802150835'}
            else:
                print(payee_account, amount, result['sub_msg'], result["out_biz_no"])
                data['payee_account'] = payee_account
                data['amount'] = amount
                data['payee_real_name'] = payee_real_name
                data['out_biz_no'] = result['out_biz_no']
                data['status'] = result['sub_msg']
                # error = [payee_account, amount, payee_real_name, result['sub_msg'], result['out_biz_no']]
                return data
        except:
            # print(payee_account, amount, result['sub_msg'], result["out_biz_no"])
            data['payee_account'] = payee_account
            data['amount'] = amount
            data['payee_real_name'] = payee_real_name
            data['out_biz_no'] = result['out_biz_no']
            data['status'] = "账号问题，转账失败！！！！！！！"
            # error = [payee_account, amount, payee_real_name, result['sub_msg'], result['out_biz_no']]
            return data


# def run(path):
    # file = read_excel(path)
    # pay = Payment(2018080160762939)
    # data = []
    # error = []
    # for item in file:
        # res = pay.pay(item[1], item[0], item[3], item[2])
        # res['remark'] = item[4]
        # try:   # 尝试读取第5列数据，如果没有则是新表，则将返回的数据直接写入到数据库中,否则为修改之后的表，更新原来的状态
            # out_biz_no = item[5]
            # if out_biz_no:
                # models.WebsitePayment.objects.filter(out_biz_no=out_biz_no).update(**res)
        # except Exception as e:
            # data.append(res)
        # if res['status'] != '转账成功':
            # error.append([res['payee_account'], res['amount'], res['payee_real_name'], res['remark'], res['status'],
                          # res['out_biz_no']])

    # write(data)  # 写入数据库
    # return error  # 网页返回错误信息





# 沙箱测试
# def run(path):
#     file = read_excel(path)
#     print(1)
#     pay = Payment(2016091700528570,url="https://openapi.alipaydev.com/gateway.do")
#     print(2)
#     for item in file:
#         pay.pay(item[1], item[0], item[3], item[2])
#
#
# run('../files/2018.7.30.xls')












# # 支付宝单笔转账
# from utils.read_excel import read_excel
# from utils.pay_record import write
# from datetime import datetime
# from alipay import AliPay
# from website import models
# import os, time, random
#
# current_path = os.path.dirname(__file__)
#
#
# class Payment():
#     def __init__(self, appid, url="https://openapi.alipay.com/gateway.do"):
#         """
#         支付接口初始化
#         :param appid: 商户appid
#         :param url: 支付宝接口url
#         """
#         self.app_private_key_string = open(current_path + "/app_private_key.txt").read()  # 应用私钥（默认从两个TXT文件中读取）
#         self.alipay_public_key_string = open(current_path + "/alipay_public_key.txt").read()  # 支付宝公钥
#         self.alipay = AliPay(
#             appid=appid,
#             app_notify_url=url,
#             app_private_key_string=self.app_private_key_string,
#             alipay_public_key_string=self.alipay_public_key_string,
#             sign_type="RSA2",
#             debug=False
#         )
#
#     def pay(self, payee_account, amount, payee_real_name=None, remark=None, device=None, operator=None,
#             payer_show_name=None, payee_type="ALIPAY_LOGONID"):
#         """
#         发起转账
#         :param payee_account: 收款方账户
#         :param amount: 转账金额
#         :param payee_real_name:收款方姓名
#         :param remark: 转账备注
#         :param device: 提交设备号
#         :param operator: 转账执行人
#         :param payer_show_name: 付款方姓名
#         :param payee_type: 收款方类型
#         :return:
#         """
#         res = {'code': 0, 'message': "", 'data': {}}
#         try:
#             out_biz_no = datetime.now().strftime("%Y%m%d%H%M%S") + str(random.randint(1000, 9999))
#             result = self.alipay.api_alipay_fund_trans_toaccount_transfer(
#                 out_biz_no=out_biz_no,
#                 payee_type=payee_type,  # 收款方账户类型
#                 payee_account=payee_account,  # 收款方账户
#                 amount=amount,  # 转账金额
#                 payee_real_name=payee_real_name,  # 收款方姓名（可选，若不匹配则转账失败）
#                 remark=remark,  # 转账备注
#                 payer_show_name=payer_show_name  # 付款方姓名
#             )
#             data = {'payee_account': None, 'amount': None, 'payee_real_name': None, 'remark': device, 'order_id': None,
#                     'out_biz_no': None, 'pay_date': None, 'status': None, 'operator': operator}
#             # result={'code':'10000','msg':'Success','order_id': '','out_biz_no': '',  'pay_date':'2017-06-26 14:36:25'}
#             # 接口文档：https://docs.open.alipay.com/api_28/alipay.fund.trans.toaccount.transfer
#             if result['code'] == '10000':
#                 if result['msg'] == "Success":
#                     print(payee_account + "  转账成功" + "  交易单号：" + result["out_biz_no"])
#                 data['payee_account'] = payee_account
#                 data['amount'] = amount
#                 data['payee_real_name'] = payee_real_name
#                 data['order_id'] = result['order_id']
#                 data['out_biz_no'] = result['out_biz_no']
#                 data['pay_date'] = result['pay_date']
#                 data['status'] = '转账成功'
#             # 转账失败
#             # result={'code':'40004','msg':'Business Failed','sub_code':'PAYEE_USER_INFO_ERROR','sub_msg':
#             # '支付宝账号和姓名不匹配，请确认姓名是否正确', 'out_biz_no': '20180802150835'}
#             else:
#                 print(payee_account, amount, result['sub_msg'], result["out_biz_no"])
#                 data['payee_account'] = payee_account
#                 data['amount'] = amount
#                 data['payee_real_name'] = payee_real_name
#                 data['out_biz_no'] = result['out_biz_no']
#                 data['status'] = result['sub_msg']
#                 # error = [payee_account, amount, payee_real_name, result['sub_msg'], result['out_biz_no']]
#             res['data']['resMessage'] = data['status']
#
#             try:
#                 models.WebsitePayment.objects.create(**data)
#             except Exception as e:
#                 res['code'] = 1
#                 res['message'] = e.__repr__()
#                 res['data']['resMessage'] = '转账完成，数据库写入出错，请记录信息，以便手动导入。'
#
#         except Exception as e:
#             res['code'] = 2
#             res['message'] = e.__repr__()
#             res['data']['resMessage'] = '转账失败'
#         return res














# def run(path):
#     file = read_excel(path)
#     pay = Payment(2018080160762939)
#     data = []
#     error = []
#     for item in file:
#         res = pay.pay(item[1], item[0], item[3], item[2])
#         res['remark'] = item[4]
#         try:   # 尝试读取第5列数据，如果没有则是新表，则将返回的数据直接写入到数据库中,否则为修改之后的表，更新原来的状态
#             out_biz_no = item[5]
#             if out_biz_no:
#                 models.WebsitePayment.objects.filter(out_biz_no=out_biz_no).update(**res)
#         except Exception as e:
#             data.append(res)
#             write(data)
#             data = []
#         if res['status'] != '转账成功':
#             error.append([res['payee_account'], res['amount'], res['payee_real_name'], res['remark'], res['status'],
#                           res['out_biz_no']])
#
#     write(data)  # 写入数据库
#     return error  # 网页返回错误信息

# run('../files/2018.7.30.xls')


# 沙箱测试
# def run(path):
#     file = read_excel(path)
#     print(1)
#     pay = Payment(2016091700528570,url="https://openapi.alipaydev.com/gateway.do")
#     print(2)
#     for item in file:
#         pay.pay(item[1], item[0], item[3], item[2])
#
#
# run('../files/2018.7.30.xls')
