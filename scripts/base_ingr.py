from ..utils import ingredient_class, product_encoder, node_class

import sys

def calBaseComponent(node):
    def dictAdd(d1, d2, mul):
        for p in d2.items():
            d1[p[0]] += p[1] * mul

    d = {
        '瑞士卷木柴': 0, '豆豆果凍': 0, '方糖': 0,
        '餅乾粉': 0, '果凍莓': 0, '香醇牛奶': 0, '棉花糖羊毛': 0
    }
    if isinstance(node.item, node_class.Base):
        d[node.item.name] = 1
    else:
        for n in node.in_nodes:
            dictAdd(d, n.d, node.getReqAmt(n))
    node.d = d

def printBaseComponent(nodes, fout=sys.stdout):
    for n in nodes:
        print(f"{n.item.name}", file=fout)
        item_ls = [p for p in n.d.items() if p[1] != 0]
        for i, p in enumerate(item_ls):
            if i == len(item_ls) - 1:
                print(f'    └── {p[0]}:{p[1]} ', file=fout)
            else:
                print(f'    ├── {p[0]}:{p[1]} ', file=fout)
        print(file=fout)

def printAllIngr(node, prefix='', fout=sys.stdout, is_first=False, mul=1):
    # ref. https://github.com/kddeisz/tree/blob/master/tree.py
    if is_first: print(prefix + node.item.name, file=fout)

    for i, cur_node in enumerate(node.in_nodes):
        if i == len(node.in_nodes) - 1:
            print(prefix + '└── ' + f'{cur_node.item.name} ({node.getReqAmt(cur_node)})', file=fout)
            printAllIngr(cur_node, prefix + '    ', fout=fout)
        else:
            print(prefix + '├── ' + f'{cur_node.item.name} ({node.getReqAmt(cur_node)})', file=fout)
            printAllIngr(cur_node, prefix + '│   ', fout=fout)

def printBaseRank(nodes, fout=sys.stdout):
    # sort things first
    from collections import defaultdict
    d = defaultdict(list)
    for node in nodes:
        for name, cnt in node.d.items():
            d[name].append((node.item.name, cnt))
    for name, ls in d.items():
        ls_sorted = sorted(ls, lambda x: x[1])
        print(name, file=fout)
        for i in enumerate(ls_sorted):
            if i == len(ls_sorted) - 1: 
                print(f'    └── {i[0]}: {i[1]}', file=fout)
            else:
                print(f'    ├── {i[0]}: {i[1]}', file=fout)
        print(file=fout)

# ---------------

def outputCraftTree(nodes, fout=sys.stdout, minimal=True):
    print("The crafting branch only show the recipe for one thing", file=fout)
    print("If you want to know how much base material is used in total, see base_ingr.txt", file=fout)
    print(file=fout)
    iter_ls = nodes if not minimal \
              else [n for n in nodes if n.out_deg == 0]
    for i in iter_ls:
        if isinstance(i.item, node_class.Base): continue
        printAllIngr(i, '', True)
        print(file=fout)

def outputBaseIngredients(nodes, fout=sys.stdout):
    node_class.Node.topologicalWalk(nodes, calBaseComponent)
    printBaseComponent(nodes)

def outputBaseIngredientsXML(nodes, fout=sys.stdout):
    "fout needs to be "