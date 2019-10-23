# -*- coding: utf-8 -*-
import time

import top.api
import datetime
import traceback
appkey = '25107266'
secret = 'fd9c81803e051c51bfab837be79e4e18'
sessionkey = '70000100643f167aa54097f45a76bad3a343c40ac9fe1fb172810cf14dda7be378d23ae2486660769'
req=top.api.TbkScOrderGetRequest()
req.set_app_info(top.appinfo(appkey,secret))

req.fields="tb_trade_parent_id,tb_trade_id,num_iid,item_title,item_num,price,pay_price,seller_nick,seller_shop_title,commission,commission_rate,unid,create_time,earning_time,tk3rd_pub_id,tk3rd_site_id,tk3rd_adzone_id,relation_id,tb_trade_parent_id,tb_trade_id,num_iid,item_title,item_num,price,pay_price,seller_nick,seller_shop_title,commission,commission_rate,unid,create_time,earning_time,tk3rd_pub_id,tk3rd_site_id,tk3rd_adzone_id,special_id,click_time"
req.span=1200
req.tk_status=1
req.order_query_type='create_time'
req.start_time = "2018-11-11 00:00:00"
# req.page_size = 100
result = []
count = 0
for i in range(3 * 24):
    time.sleep(0.5)
    req.start_time=(datetime.datetime.strptime(req.start_time , "%Y-%m-%d %H:%M:%S") + datetime.timedelta(minutes=20)).strftime("%Y-%m-%d %H:%M:%S")
    # print(req.start_time)
    try:
        resp= req.getResponse(sessionkey)
        if 'n_tbk_order' in resp['tbk_sc_order_get_response']['results']:
            result.extend(resp['tbk_sc_order_get_response']['results']['n_tbk_order'])
            count += len(resp['tbk_sc_order_get_response']['results']['n_tbk_order'])
        # print(resp)
    except Exception as e:
        traceback.print_exc()
        print(e)
print(result)
print(len(result))
print(count)
#
# resp= req.getResponse(sessionkey)
# print(resp)