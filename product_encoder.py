from ingredient_class import *

def encode(base_list, compound_list):
    for i in base_list:
        print(f'{i.name}: Base, {i.cost}, {i.time}, {i.value}')
    for i in compound_list:
        print(f'{i.name}: Compound, {i.time}, {i.value}, ', end='')
        print(','.join([f'{p[0]}:{p[1]}' for p in i.ingredients]))


def readBase(ls):
    # e.g. '香醇牛奶: Base, 350.0, 900.0, 1865'
    name = ls[0][:-1]
    cost = float(ls[2][:-1])
    time = float(ls[3][:-1])
    sell_value = int(ls[4])
    return Base(name, cost, time, sell_value)

def readCompound(ls):
    # e.g. '恆久的糖衣槌子: Compound, 21600, 18045, 瑞士卷木柴:30,方糖:35'
    name = ls[0][:-1]
    time = int(ls[2][:-1])
    value = float(ls[3][:-1])
    
    ing_ls = []
    if len(ls) == 5:
        for ing in ls[4].split(','):
            # ing = '瑞士卷木柴:30'
            ing_subls = ing.split(':')
            ing_ls.append((ing_subls[0], int(ing_subls[1])))
    return Compound(name, ing_ls, value, time)
    

def decode(fname):
    base_list = []
    compound_list = []
    with open(fname, 'r') as fin:
        str_ls = fin.readlines()
        for in_str in str_ls:
            if in_str.strip() == "" or in_str[0] == '#':
                continue
            ls = in_str.strip().split(' ')
            if 'Compound' in ls[1]:
                compound_list.append(readCompound(ls))
            elif 'Base' in ls[1]:
                base_list.append(readBase(ls))
    return base_list, compound_list