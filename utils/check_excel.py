"""
    ref. https://forum.gamer.com.tw/C.php?bsn=70199&snA=1367&tnum=6&bPage=2
    Check the difference between HoyfSam1's data and products.txt
    Note that some of the names were different:

    薑餅人王國資訊(line)            HoyfSam1

    神秘蝴蝶餅木樁        <->     神秘蝴蠂餅木樁
    恆久的糖衣槌子        <->     恆久的糖衣鎚子
    糖果奶油義大利麵      <->     糖果奶油意大利麵
    玻璃捧花             <->     玻璃棒花
    新鮮草莓蛋糕          <->     新鮮草莓蛋禚
    糖衣戒指             <->     糖衣戎指
    皇家熊熊果凍王冠      <->    皇家熊熊果凍皇冠

"""


import .ingredient_class
import .node_class
import .product_encoder
import openpyxl
import re

# makes all things
base_ls, component_ls = product_encoder.decode('products.txt')
node_dict = node_class.make_nodes(base_ls, component_ls)
nodes = list(node_dict.values())

# get excel
wb = openpyxl.load_workbook('/mnt/e/download_file/薑餅人王國：各產物相關資料upgrade.xlsx')
wbsheet = wb['生產效率']

for i in range(13, 108):
    # B: name
    name = wbsheet[f'B{i}'].value
    if name is None or name.strip() in ['', '物品']:
        continue

    # D: time, (s|m|h)
    time_dict = {'s': 1, 'm': 60, 'h': 3600}
    time = 0
    for p in re.findall('([0-9]+)(s|m|h)', wbsheet[f'D{i}'].value):
        # p = ('7', 'h'), etc
        time += int(p[0]) * time_dict[p[1]]
    
    # E: ingredients, '香醇牛奶*10、咕咕鐘*1'
    ing_ls = []
    ls = wbsheet[f'E{i}'].value.split('、') # ls = ['香醇牛奶*10', '咕咕鐘*1']
    for s in ls:
        ing = s.split('*')  # ing = ['香醇牛奶', '10']
        ing[1] = int(ing[1])
        ing_ls.append(tuple(ing))
    
    # H: value
    value = int(wbsheet[f'H{i}'].value)

    try:
        item = node_dict[name].item
    except:
        print(f'{name} not exist in products.txt')
        continue

    if item.value != value:
        print(f'{name}\'s value is wrong: should be {value}, not {item.value}')
    if item.time != time:
        print(f'{name}\'s time is wrong: should be {time}, not {item.time}')
    if len(item.ingredients) != len(ing_ls):
        print(f'{name}\'s ingredient is wrong: {item.ingredients}, {ing_ls}')
        continue
    for a in item.ingredients:
        if a not in ing_ls:
            print(f'{name}\'s ingredient is wrong: {item.ingredients}, {ing_ls}')
            break
            

        
