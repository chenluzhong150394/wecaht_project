# coding=utf-8
import os
import json
import mysql.connector


def data_conn(token):
    print('wechat' + '@' + '127.0.0.1' + ':' + '3306')
    conn = mysql.connector.connect(
    host='127.0.0.1',
    port=3306,
    user='wechat',
    password='tenew123456',
    charset='utf8mb4',
    database = 'wechat',
    )
    cursor = conn.cursor()
    sql = """ UPDATE wechat.website_token SET token = '%s' WHERE id = 1 """ % token
    content = cursor.execute(sql)
    conn.commit()
    #data_result = list(cursor.fetchall())
    cursor.close()
    conn.close()
    #return data_result


def get_acesstoken():
    shell = 'curl "https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=wx915151a971f177d2&secret=a8f7e885da39a7e346827c74b5282e53"'
    res = os.popen(shell).readlines()
    res = json.loads(res[0])
    token = res['access_token']
    res = data_conn(token)

get_acesstoken()

