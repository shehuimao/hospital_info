import requests
import time
def get_mercator(addr):
    url= 'http://api.map.baidu.com/geocoder/v2/?address=%s&output=json&ak=CGoVCg9cBhy02I0ZDg9GZmbdvxuLIFFI&callback=showLocation'%(addr)
    response = requests.get(url)
    return response.text
def TXTRead_Writeline(src,dest):
    ms = open(src,encoding='utf-8')
    for line in ms.readlines():
        with open(dest,"a",encoding='utf-8') as mon:
            loc=get_mercator(line)
            mon.write(loc)
            mon.write("\n")
            time.sleep(1)
TXTRead_Writeline("D:\data\\address.txt","D:\data\\address_result.txt")