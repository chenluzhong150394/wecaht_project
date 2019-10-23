from utils.payment_interface import Payment
from utils.read_excel import read_excel

def run():
    file = read_excel('../files/2018.7.30(1).xls')
    Pay = Payment(2016091700528570)
    for item in file:
        print(item)
        Pay.pay(item[1],item[0],item[3],item[2])


run()