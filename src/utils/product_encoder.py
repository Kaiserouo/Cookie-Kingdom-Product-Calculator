from .ingredient_class import *
from typing import *

def encode(base_list: List[Base], compound_list: List[Compound]):
    for i in base_list:
        print(f'{i.name}: Base, {i.cost}, {i.time}, {i.value}')
    for i in compound_list:
        print(f'{i.name}: Compound, {i.time}, {i.value}, ', end='')
        print(','.join([f'{p[0]}:{p[1]}' for p in i.ingredients]))


def readBase(ls: List[str]) -> Base:
    # e.g. '香醇牛奶: Base, 350.0, 900.0, 1865'
    name = ls[0][:-1]
    cost = float(ls[2][:-1])
    time = float(ls[3][:-1])
    sell_value = int(ls[4])
    return Base(name, cost, time, sell_value)

def readCompound(ls: List[str]) -> Compound:
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
    

def decode(
        fname: str
        ) -> Tuple[List[Base], List[Compound], List[Tuple[str, List[Product]]]]:
    base_list = []
    compound_list = []
    factory_list = []

    current_factory = None
    with open(fname, 'r', encoding='utf-8') as fin:
        str_ls = fin.readlines()
        for in_str in str_ls:
            # comment
            if in_str[0] == '#':
                continue
            # factory
            if in_str[0] == '>':
                current_factory = (' '.join(in_str.split()[1:]), [])
                factory_list.append(current_factory)
                continue
            # blank line
            if in_str.strip() == "":
                current_factory = None
                continue

            ls = in_str.strip().split()
            if 'Compound' in ls[1]:
                compound_list.append(cur_node := readCompound(ls))
            elif 'Base' in ls[1]:
                base_list.append(cur_node := readBase(ls))
                
            if current_factory != None:
                current_factory[1].append(cur_node)

    return base_list, compound_list, factory_list
    