import requests, xlwt
import xlwings as xw
from bs4 import BeautifulSoup
import os

# 初始化
def init():
    global url, province_name, yiyuan_jibie, headers
    url = 'http://www.yixue.com/'
    province_name = [
        '北京市', '天津市', '河北省', '山西省', '辽宁省', '吉林省', '黑龙江省', '上海市',
        '江苏省', '浙江省', '安徽省', '福建省', '江西省', '山东省', '河南省', '湖北省',
        '湖南省', '广东省', '内蒙古自治区', '广西壮族自治区', '海南省', '重庆市', '四川省', '贵州省',
        '云南省', '西藏自治区', '陕西省', '甘肃省', '青海省', '宁夏回族自治区', '新疆维吾尔自治区'
    ]

    yiyuan_jibie = ["三级甲等", "三级乙等", "三级丙等", "二级甲等", "二级乙等", "二级丙等", "一级甲等", "一级乙等", "一级丙等"]
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

    # 创建文件夹存不同等级的医院列表
    for jibie in yiyuan_jibie:
        mkpath = r'C:/Users/lurong.mao/Desktop/医院信息爬虫数据/分等级/' + jibie
        os.mkdir(mkpath)

#将信息写入EXCEL表中
def sav_message(messgae, province_now,jibie):
    #创建workbook
    workbook = xlwt.Workbook(encoding='utf-8')
    name = str(province_now) + str(jibie) + "医院列表"
    table = workbook.add_sheet(name)
    value = ["医院名称", "医院地址", "联系电话", "重点科室", "经营方式", "传真号码", "电子邮箱", "医院网站"]
    #表头 table.write(行,列,值)
    for i in range(len(value)):
        table.write(0,i,value[i])
    i = 0
    #for data in messgae[3]:
    for data in messgae[4]:
        #在这会出现有的地区没有二丙等级别的医院，所以NONE。判断跳过
        if len(data) <= 1:
            break
        else:
            #江苏省一级甲等 无锡市滨湖区荣巷医院?无锡和平骨科医院 <a>标签缺失。写一个try except 语句跳过
            try:
                #写入医院名称
                table.write(i+1, 0, data.b.a.text)
                for data_1 in data.ul:
                    now_mess = data_1.text.replace('\n', '')
                    now_data = now_mess.split('：')
                    count = 0
                    #医院名称:北京协和医院  通过判断医院名称等信息位置是否准确，填入后面各医院信息
                    for tittle in value:
                        if tittle == now_data[0]:
                            index = count
                        count = count + 1
                    table.write(i+1, index, now_data[1])
                i = i + 1
            except:
                print(data.b.text + "这家医院爬取失败")
    workbook.save(r'C:/Users/lurong.mao/Desktop/医院信息爬虫数据/分等级/'+str(jibie)+'/'+str(province_now) + '医院列表.xls')

#获取当前省数据
def get_province_hospital(province_now,jibie):
    #print(url+province_now+jibie+'医院列表')
    r = requests.get(str(url)+str(province_now)+str(jibie)+str('医院列表'),headers=headers,timeout=30)
    soup = BeautifulSoup(r.text, "lxml")

    message = soup.find_all('ul')

    sav_message(message, province_now,jibie)
#主函数
if __name__ == '__main__':
    init()
    for province in province_name:
        for jibie in yiyuan_jibie:
            get_province_hospital(province,jibie)

for jibie in yiyuan_jibie:
    for xl in yiyuan_jibie:
        xlpath = r'C:/Users/lurong.mao/Desktop/医院信息爬虫数据/分等级/' + jibie + '/' + xl
        wb = xw.Book(xlpath)
        sht = wb.sheets[0]
        nrows = sht.api.UsedRange.Rows.count
        #在 I1:I{nrows} 区间插入 级别
        sht.range(f'I1:I{nrows}').value = jibie
        wb.save()
        wb.close()


