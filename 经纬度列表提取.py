# -*- coding:utf-8 -*-
import json
with open("address_result.json", 'r', encoding='utf-8') as f:
    new1 = []
    for line in f.readlines():
        temp = json.loads(line)
        new1.append(temp)
print(new1)
print(new1[0]['result']['location']['lng'],new1[0]['result']['location']['lat'])
print(len(new1))

for item in new1:
    a = item['result']['location']['lng']
    b = item['result']['location']['lat']
    print(b)





