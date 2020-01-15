# coding=utf-8
import os
import json
import mysql.connector


def data_conn(token):
    print('开始写入acesstoken')
    # print('wechat' + '@' + '127.0.0.1' + ':' + '3306')
    conn = mysql.connector.connect(
    host='47.98.50.15',
    port=3306,
    user='clz',
    password='oracle',
    charset='utf8',
    database = 'clz',
    )
    cursor = conn.cursor()
    print(token)
    sql = """ UPDATE clz.website_token SET token = '%s' WHERE id = 1 """ % token
    content = cursor.execute(sql)
    conn.commit()
    #data_result = list(cursor.fetchall())
    cursor.close()
    conn.close()
    #return data_result


def get_acesstoken():
    shell = 'curl "https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=wx1e15cce8c4e924ef&secret=86bc1fe693a8276f3c3618b84e349bd3"'
    res = os.popen(shell).readlines()
    res = json.loads(res[0])
    print(res)
    token = res['access_token']
    res = data_conn(token)

get_acesstoken()

