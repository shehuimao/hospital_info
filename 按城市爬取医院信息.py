import random
import requests
from bs4 import BeautifulSoup
import re
from xpinyin import Pinyin


# 自动寻找下一个接龙城市
# 函数参数c表示城市名字，total_CityPinyin_list表示全国城市拼音列表，city_list表示全国城市列表，
# city_list_copy表示全国城市列表的副本，用于保存剩余未被下载过的城市名，以防重复请求下载。
def get_NextCiyt(c , total_CityPinyin_list , city_list , city_list_copy):
    city_list_copy.remove(c) #以防重复下载
    if not city_list_copy:  #下载完所有城市后，返回None停止请求
        return None
    in_py_list = p.get_pinyin(c , ' ').split(' ')
    total_city_len = len(total_CityPinyin_list)
    next_city = None
    #寻找接龙城市
    for i in range(total_city_len):
        if in_py_list[1] == total_CityPinyin_list[i][0]:
            if total_city_len == len(city_list):
                next_city = city_list[i]
                break
    if next_city:
        return next_city
    else:
        #当无法接龙时，随机选一城市
        print('not found city')
        return random.choice(city_list_copy)


# 解析各医院信息
def parse_hospital(city_name):
    response = requests.get(url='http://www.a-hospital.com/w/{0}医院列表'.format(city_name), headers=headers, timeout=15)
    # selector = Selector(response)
    soup = BeautifulSoup(response.text, 'lxml', from_encoding='utf-8')
    useful_info = soup.find(id='bodyContent')
    useful_info = useful_info.find_all('ul', recursive=False)

    for i in useful_info:
        info_raw = i.find_all('li', recursive=False)
        count = 0
        for j in info_raw:
            count += 1
            hospital_info = j.text
            try:
                address = re.search('医院地址：(.*?)\n', hospital_info).group(1)
            except:
                break
            name = re.search('^(.*?)\n', hospital_info).group(1)
            name_md5 = DelDuplicate(name)
            if name_md5 in name_only:
                print('the hospital is parsed , pass!')
                continue
            name_only.add(name_md5)
            match_obj = re.search('联系电话：(.*?)\n', hospital_info)
            if match_obj:
                phone = match_obj.group(1)
            else:
                phone = None
            match_obj = re.search('医院等级：(.*?)\n', hospital_info)
            if match_obj:
                rate = match_obj.group(1)
            else:
                rate = None
            match_obj = re.search('重点科室：(.*?)\n', hospital_info)
            if match_obj:
                important_item = match_obj.group(1)
            else:
                important_item = None
            match_obj = re.search('传真号码：(.*?)\n', hospital_info)
            if match_obj:
                fax_number = match_obj.group(1)
            else:
                fax_number = None
            match_obj = re.search('经营方式：(.*?)\n', hospital_info)
            if match_obj:
                business_model = match_obj.group(1)
            else:
                business_model = None
            match_obj = re.search('电子邮箱：(.*?)\n', hospital_info)
            if match_obj:
                e_mail = match_obj.group(1)
            else:
                e_mail = None
            match_obj = re.search('医院网站：(.*?)\n', hospital_info)
            if match_obj:
                website = match_obj.group(1)
            else:
                website = None
            print('number %s' % count, ' ', name)
            params = (name, address, phone, rate, important_item, fax_number, business_model, e_mail, website)
            insert_to_sql(params)
    with open(r'C:\Users\Administrator\Desktop\小库科技编程题\name_only.txt', 'w') as wf:
        wf.write(str(name_only))


