import requests, re, xlwt, datetime
from bs4 import BeautifulSoup


# 初始化
def init():
    global url, province_name, headers
    url = 'http://www.yixue.com/'
    province_name = [
        '北京市', '天津市', '河北省', '山西省', '辽宁省', '吉林省', '黑龙江省', '上海市',
        '江苏省', '浙江省', '安徽省', '福建省', '江西省', '山东省', '河南省', '湖北省',
        '湖南省', '广东省', '内蒙古自治区', '广西壮族自治区', '海南省', '重庆市', '四川省', '贵州省',
        '云南省', '西藏自治区', '陕西省', '甘肃省', '青海省', '宁夏回族自治区', '新疆维吾尔自治区'
    ]
    headers = {
        'Host': 'www.yixue.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'

    }


#存储数据
def sav_message(messgae, province_now):
    workbook = xlwt.Workbook(encoding='utf-8')
    name = province_now + "医院列表"
    table = workbook.add_sheet(name)
    value = ["医院名称", "医院地址", "联系电话", "医院等级", "重点科室", "经营方式", "传真号码", "电子邮箱", "医院网站"]
    for i in range(len(value)):
        table.write(0, i, value[i])
    i = 0
    for data in messgae[3]:
        table.write(i + 1, 0, data.b.a.text)
        for data_1 in data.ul:
            now_mess = data_1.text.replace('\n', '')
            now_data = now_mess.split('：')
            count = 0
            for tittle in value:
                if tittle == now_data[0]:
                    index = count
                count = count + 1
            table.write(i + 1, index, now_data[1])
        i = i + 1
    workbook.save('D:/医院信息爬虫数据/' + province_now + '医院列表.xls')


# 获取当前省数据
def get_province_hospital(province_now):
    r = requests.get(url + province_now + '医院列表', headers=headers, timeout=10)
    soup = BeautifulSoup(r.text, "lxml")
    message = soup.find_all('ul')
    sav_message(message, province_now)


#主函数
if __name__ == '__main__':
    init()
    for province in province_name:
        get_province_hospital(province)