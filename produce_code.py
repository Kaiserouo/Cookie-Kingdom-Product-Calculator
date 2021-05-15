"""
    Given input of factory information from "薑餅人王國資訊",
    produce formatted code to use in ingredient_class.
    
    Uses 'product_value.dat' to get value. Need form '<name> <value>'

    Output [] if ingredient is '待補充'
    Output 0 if value not available from 'product_value.dat'

    Now only support compound-type ingredient

    e.g. 
        可愛娃娃工坊/Lv.3
        Lv.1雲朵糖抱枕 1(1小時30分鐘/糖果花 1、棉花糖羊毛 1)
        Lv.2熊熊果凍娃娃 1(4小時/糖果花束 2、棉花糖羊毛 1)
        Lv.3火龍果龍族娃娃 1(7小時/待補充)

        建造：9小時/瑞士卷木柴 50、松果鳥娃娃 8、神秘蝴蝶餅木樁 1
        升級Lv.2：15小時/極光柱子 15、咕咕鐘 1、藍色糖果鉗子 2
        升級Lv.3：待補充
    ->
        Compound('雲朵糖抱枕', [('糖果花', 1), ('棉花糖羊毛', 1)],
                14722,      5400),
        Compound('熊熊果凍娃娃', [('糖果花束', 2), ('棉花糖羊毛', 1)],
                24806,      14400),
        Compound('火龍果龍族娃娃', [],
                0   ,      25200),
"""

import re

def processInput(s):
    # return [(name, count), time_second, [ingredients]]

    # group by regex,    Lv.3椪糖果醬 1(20分鐘/豆豆果凍 6、紮實的黑麥麵包 2)
    #                 -> ('Lv.3', '椪糖果醬 1', '20分鐘', '豆豆果凍 6、紮實的黑麥麵包 2')
    ret_ls = []
    ls = re.match(r"(Lv.[0-9])(.*)\((.*)/(.*)\)", s).groups()
    
    # ----- (name, count) -----
    ret_ls.append( tuple(ls[1].split(' ')) )

    # ----- time_seconds -----
    time_dict = { '小時': 3600,  '分鐘': 60,  '秒': 1 }
    # time_ls = [('1', '小時'), ('20', '分鐘')] (as an example)
    time_ls = re.findall('([0-9]*)(分鐘|小時|秒)', ls[2])
    time = 0
    for i in time_ls: time += int(i[0]) * time_dict[i[1]]
    ret_ls.append(time)

    # ----- [ingredients] -----
    if ls[3] == '待補充':
        ret_ls.append([])
    else:
        ingstr_ls = ls[3].split('、')
        ing_ls = []
        for i in ingstr_ls:
            tmp = i.split(' ')
            tmp[1] = int(tmp[1])
            ing_ls.append(tuple(tmp))
        ret_ls.append(ing_ls)

    # result: [('椪糖果醬', '1'), 1200, [('豆豆果凍', 6), ('紮實的黑麥麵包', 2)]]
    return ret_ls

def readValueDict(fname):
    d = dict()
    with open(fname, 'r') as fin:
        while (i := fin.readline()) != "":
            l = i.split(' ')
            d[l[0]] = int(l[1])
    return d

value_dict = readValueDict('product_value.dat')

input()
while (k := input().strip()) != '':
    k = k.strip()
    # ls = [('石榴果醬', '1'), 7200, [('豆豆果凍', 16), ('果凍拿鐵', 1)]]
    ls = processInput(k)
    print(ls)
    try:
        print(
            f"    Compound('{ls[0][0]}', {ls[2]},\n            {value_dict[ls[0][0]]},      {ls[1]}),"
        )
    except KeyError:
        print(
            f"    Compound('{ls[0][0]}', {ls[2]},\n            0   ,      {ls[1]}),"
        )