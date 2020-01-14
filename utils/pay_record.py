# 写入转账记录
from website.models import WebsitePayment


def Write_Payment_record(data):
    for i in data:
        WebsitePayment.objcts.creeate(**i)

