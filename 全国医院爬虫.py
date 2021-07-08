import requests, re, xlwt, datetime
from bs4 import BeautifulSoup


# 初始化
def init():
    global url, headers
    url = 'https://www.zgylbx.com/index.php?m=content&c=index&a=lists&catid=106&page='
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.8",
        "Cache-Control": "max-age=0",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.86 Safari/537.36"
    }


def sav_message(messgae):
    workbook = xlwt.Workbook(encoding='utf-8')
    name = "中国医疗保险网" + str(i)
    table = workbook.add_sheet(name)
    value = ["医院名称", "医院等级"]
    for l in range(len(value)):
        table.write(0, l, value[l])

    m = 0
    j = 0

    for j in range(1, 40):
        if j % 2 == 1:
            data = messgae[j].find_all('td')
            # 写入数据 write(行,列,值)
            table.write(m + 1, 0, data[0].text)
            table.write(m + 1, 1, data[2].text)
            m = m + 1

    workbook.save(r'C:/Users/lurong.mao/Desktop/中国医疗保险网/' + name + '.xls')


def get_jiegou(url):
    global i
    for i in range(1, 1530, 1):
        # https://www.zgylbx.com/index.php?m=content&c=index&a=lists&catid=106&page=0&k1=0&k2=0&k3=0&k4=
        r = requests.get(str(url) + str(i) + "&k1=0&k2=0&k3=0&k4=", headers=headers, timeout=20)
        print(str(url) + str(i) + "&k1=0&k2=0&k3=0&k4=")
        soup = BeautifulSoup(r.text, "lxml")
        message = soup.find_all('tr')
        # print(message)
        sav_message(message)


if __name__ == '__main__':
    init()
    get_jiegou(url)