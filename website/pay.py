# -*- coding: utf-8 -*-
import time
from OA import settings
from django.core import cache
from _md5 import md5
from uuid import uuid4
from datetime import datetime
from website import models
from .utils1 import create_mch_billno
import requests

try:
    cache = cache.get_cache('general')
except Exception:
    cache = cache.cache



SENDREDPACK_URL = 'https://api.mch.weixin.qq.com/mmpaymkttransfers/sendredpack'


def sign(params):
    '''
    https://pay.weixin.qq.com/wiki/doc/api/tools/cash_coupon.php?chapter=4_3
    '''
    params = [(str(key), str(val)) for key, val in params.iteritems() if val]
    sorted_params_string = '&'.join('='.join(pair) for pair in sorted(params))
    sign = '{}&key={}'.format(sorted_params_string, settings.WEIXIN_PAY_API_KEY)
    return md5(sign).hexdigest().upper()


def sendredpack():
    info = models.TransferRecord.objects.filter(status=0).all()
    for i in info:
        re_openid = i.re_openid
        total_amount = i.total_amount
        mch_billno = i.mch_billno
        total_num = 1,
        send_name = u'发送者',
        wishing = '',
        act_name = '',
        remark = '',
        client_ip = '49.235.100.45'
        randuuid = uuid4()
        nonce_str = str(randuuid).replace('-', '')
        mch_id = settings.WEINXIN_PAY_MCH_ID
        wxappid = settings.WEIXIN_APP_ID
        scene_id = 'PRODUCT_2'

        params = {
            'mch_billno': mch_billno,  # 商户订单号
            'mch_id': mch_id,  # 商户号
            'wxappid': wxappid,  # 公众号APP_ID
            'send_name': send_name,  # 商户名称
            're_openid': re_openid,  # 用户open_id
            'total_amount': total_amount,  # 金额
            'total_num': total_num,  # 次数
            'wishing': wishing,  # 红包祝福语
            'client_ip': client_ip,  # ip地址
            'act_name': act_name,  # 活动名称
            'remark': remark,  # 备注
            'nonce_str': nonce_str,  # 随机字符串
            'scene_id': scene_id  # 场景id
        }
        # sign 签名
        sign_string = sign(params)

        template = '''<xml>
       <sign><![CDATA[{sign}]]></sign>
       <mch_billno><![CDATA[{mch_billno}]]></mch_billno>
       <mch_id><![CDATA[{mch_id}]]></mch_id>
       <wxappid><![CDATA[{wxappid}]]></wxappid> 
       <send_name><![CDATA[{send_name}]]></send_name> 
       <re_openid><![CDATA[{re_openid}]]></re_openid> 
       <total_amount><![CDATA[{total_amount}]]></total_amount> 
       <total_num><![CDATA[{total_num}]]></total_num> 
       <wishing><![CDATA[{wishing}]]></wishing>
       <client_ip><![CDATA[{client_ip}]]></client_ip>
       <act_name><![CDATA[{act_name}]]></act_name> 
       <remark><![CDATA[{remark}]]></remark> 
       <nonce_str><![CDATA[{nonce_str}]]></nonce_str> 
       <scene_id><![CDATA[scene_id]]></scene_id>
    </xml>
    '''
        params['sign'] = sign_string
        content = template.format(**params)
        headers = {'Content-Type': 'application/xml'}
        print(content)
        respose = requests.post(SENDREDPACK_URL, data=content, headers=headers,
                                cert=(settings.WEIXIN_PAY_CERT_PATH, settings.WEIXIN_PAY_CERT_KEY_PATH))
        print(respose)
        return respose
