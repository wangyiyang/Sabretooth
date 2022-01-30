import http.client
from json.tool import main
import mimetypes
from operator import truediv
import time
import json
import datetime


now = time.strftime("%Y%m%d", time.localtime()) 
# ['2022-01-04', '4957.98', '4917.77', '-22.60', '-0.46%', '4874.53', '4961.45', '151534784', '33651696.00', '-']


def get_shares_history(code="zs_399300", start="20220101", end=now):
    conn = http.client.HTTPSConnection("q.stock.sohu.com")
    payload = ''
    headers = {}
    query = "/hisHq?code={code}&start={start}&end={end}".format(code=code,start=start,end=end)
    conn.request("GET", query, payload, headers)
    res = conn.getresponse()
    data = res.read()
    return json.loads(data)

def AIP(money=1000, history=[]):
    a=0
    b=0
    count = 0 
    chg = 0.0
    chg_money = 0
    capital = 0 + money 
    position = 0 + money
    len_history = len(history)
    for i in range(len_history,0,-1):
        if i != len_history:
            if is_next_month(history[i-1][0],history[i][0]):
                count += 1
                capital += money
                position += money
            # if position/capital >= 1.1:
            #     a += 1
            #     position /= 2
            #     capital /= 2
            #     chg_money += position - capital
            #     if max_capital < capital:
            #         max_capital = capital
            #     print(history[i][0],position,capital,chg_money,max_capital)
            
            # if position/capital <= 0.9:
            #     b  += 1
            #     capital += position 
            #     position *= 2
            #     if max_capital < capital:
            #         max_capital = capital
            #     print(history[i][0],position,capital,chg_money,max_capital)
            position += position*str2percent(history[i][4])
            chg = position/capital
            chg_money = position - capital
            if chg > 1.3:
                print( count, chg,chg_money,capital,position,history[i][0])
    return count, chg,chg_money,capital,position

def is_next_month(istr,jstr):
    iobj = datetime.datetime.strptime(istr, "%Y-%m-%d").date()
    jobj = datetime.datetime.strptime(jstr, "%Y-%m-%d").date()
    if iobj.year < jobj.year:
        return True
    if iobj.month > jobj.month:
        return True
    return False

def str2percent(str):
    return float(str.strip('%'))/100.00

if __name__ == '__main__':
    history = get_shares_history(start="20050101")
    print(AIP(history = history[0]["hq"]))


            