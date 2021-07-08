import json
f = open("address_result.json",'r',encoding='utf-8')
ln = 0
for line in f.readlines():
    ln += 1
    dic = json.loads(line)
    t = dic['location']
    f = open("data111111.txt",'a',encoding='utf-8')
    f.writelines(str(t));f.write("\n")
f.write(str(ln))
f.close()
