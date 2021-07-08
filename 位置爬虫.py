from bs4 import BeautifulSoup
import urllib.request
import request
import requests
import re
import codecs
import time
import xlwt


class HospitalItem(object):
    HospitalName = None  # 医院名称
    HospitalLevel = None  # 医院等级
   #HospitalProperty = None  # 医院属性d
    HospitalAddress = None # 医院地址
    HospitalArea = None  # 占地面积
    HospitalBuild = None  # 建筑面积


class GetHospital(object):
    def __init__(self):
        self.urlStart = 'https://yyk.99.com.cn/zhejiang/'
        self.urlBase = 'https://yyk.99.com.cn'
        self.hospitalUrls = self.getUrls(self.urlStart)  # 拿到所有urls
        self.hospitalItems = []
        self.spider(self.hospitalUrls)  # 爬虫开始爬取
        self.pipelines(self.hospitalItems)  # 爬取的数据经过几个处理流程


    def getUrls(self, urlStart):
        print("开始获取所有url...")
        zone_index = [0 ,1 ,2 ,3 ,4 ,5 ,6 ,7 ,8 ,9 ,10]# 指定区域的下标
        hospitalUrl = []                               # 存放所有医院详情页url
        htmlContent = self.getResponseContent(urlStart)# 请求首页
        soup = BeautifulSoup(htmlContent, 'lxml')
        tables = soup.find_all('table')                # 找到所有table标签

        # 遍历各个城区
        for zi in zone_index:
            table_zone = tables[zi]
            tds = table_zone.find_all('td')            # 找到所有td标签

            # 遍历每个医院
            for td in tds:
                item_url = self.urlBase + td.a.get('href') # 获得a标签的href属性并组装目标url
                hospitalUrl.append(item_url)

        return hospitalUrl


    def getResponseContent(self ,url):
        try:
            response = urllib.request.urlopen(url)
        except:
            print('~~~~~~')
        else:
            return response.read()

# 从医院介绍提取占地面积和建筑面积
    def spider(self, urls):
        print('开始爬取数据...')
        for url in urls: # 遍历所有医院的url
            htmlContent = self.getResponseContent(url)
            soup = BeautifulSoup(htmlContent, 'lxml')
            item = HospitalItem()
            div = soup.find('div', attrs={'class': 'wrap-name'}) # 获取医院名称
            item.HospitalName = soup.find('h1').get_text()
            item.HospitalLevel = soup.find('span', attrs={'class': 'grade'}).get_text()
            hospitalAddress = soup.find('dl',attrs={'class': 'wrap-info'}).dd.find_all('p')[3].get_text()
            item.HospitalAddress = hospitalAddress.replace('地址：','')
            #hospitalProperty = soup.find('div', attrs={'class': 'wrap-info'}).dl.dd.find_all('p')[1].get_text()
            #item.HospitalProperty = hospitalProperty.replace('性质：' ,'')
            item.HospitalProperty = soup.find('span', attrs={'class': 'medical'})
            hospital_info = soup.find('div', attrs={'class': 'hospital-info'}).p.get_text()
            pattern = re.compile('[，。]?占地.*?[，。]')
            match = pattern.search(hospital_info)
            if match:
                item.HospitalArea = match[0]
            else:
                item.HospitalArea = '无'
            pattern = re.compile('[，。]?建筑面积.*?[，。]') # 获取医院建筑面积
            match = pattern.search(hospital_info)
            if match:
                item.HospitalBuild = match[0]
            else:
                item.HospitalBuild = '无'
            self.hospitalItems.append(item)

# 写入excel
    # 保存数据
    def pipelines(self, hospitalItems):
        print('开始保存数据...')
        now = time.strftime('%Y-%m-%d', time.localtime())
        fileName = 'hospital-' + now + '.xls'
        book = xlwt.Workbook(encoding='utf-8', style_compression=0) # 新建一个工作薄
        sheet = book.add_sheet('hospital')                          # 新建一个工作表
        i = 0
        while i < len(hospitalItems):                               # 遍历所有医院信息并写入
            item = hospitalItems[i]
            sheet.write(i ,0 ,item.HospitalName)
            sheet.write(i ,1 ,item.HospitalLevel)
            #sheet.write(i ,2 ,item.HospitalProperty)
            sheet.write(i ,3 ,item.HospitalAddress)
            sheet.write(i ,4 ,item.HospitalArea)
            sheet.write(i ,5 ,item.HospitalBuild)
            i = i + 1
        book.save(fileName)


if __name__ == '__main__':
    GH = GetHospital()

