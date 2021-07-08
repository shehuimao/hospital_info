import requests
import json
import xlrd
import numpy as np


def find_street(location):
    url = 'http://api.map.baidu.com/geocoder/v2'
    ak = '你的ak'
    real_url = url + '/?callback = renderReverse&location=' + location + '&output=json&pois=1&ak=' + ak
    req = requests.get(real_url)
    t = req.text
    # t=t[29:-1]
    # print(t)
    data = json.loads(t)
    street = data["result"]["addressComponent"]["street"]["street_number"]  # 输出街道名称
    return street


if __name__ == '__main__':

    path = 'lalo.xlsx'
    xl = xlrd.open_workbook(path)
    sheet = xl.sheets()[0]  # 0表示读取第一个工作表sheet
    data = []
    for i in range(2, 4):  # ncols表示按列读取
        data.append(sheet.col_values(i))
    print(np.shape(data))
    for i in range(1, np.shape(data)[1]):
        print(i)
        lat = data[1][i - 1]
        lng = data[0][i - 1]
        lat = str(lat)
        lng = str(lng)
        location = lat + ',' + lng
        street = find_street(location)
        print(street)  # 输出街道名称
