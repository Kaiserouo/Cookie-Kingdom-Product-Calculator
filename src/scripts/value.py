from ..utils import ingredient_class, product_encoder, node_class

import sys


def calValueTable(node):
    # in: ingredients
    # out: products

    # cost: ingredient cost of making it
    #     i.e. sum of all base ingredient cost needed
    # one_d_ing_value: sum of sell value of ingredients
    #                  i.e. one-depth best ingredient value search
    # best_value: best possible selling value of ingredients

    item = node.item
    node.one_d_ing_value = item.value if isinstance(item, Base) else 0
    node.cost = item.cost if isinstance(item, Base) else 0
    node.best_ing_value = item.value if isinstance(item, Base) else 0

    for n in node.in_nodes:
        node.one_d_ing_value += n.item.value * node.getReqAmt(n)
        node.best_ing_value += max(n.item.value, n.best_ing_value) * node.getReqAmt(n)
        node.cost += n.cost * node.getReqAmt(n)
    
def printValueTable(nodes, fout=sys.stdout):
    print("""\
cost: ingredient cost of making it
    i.e. sum of all base ingredient cost needed
one_d_ing_value: sum of sell value of ingredients
                 i.e. one-depth best ingredient value search
best_value: best possible selling value of ingredients
""", file=fout)
    print(f'     ing_cost(ic)    value           one_d_ing_value(odiv)     best_ing_value(biv)', file=fout)
    print(f'     value-ic        value-odiv      value-biv', file=fout)
    print(f'-------------------------------------------------------------------------------------', file=fout)
    for n in nodes:
        print(f'{n.item.name}\n     {n.cost:<15.2f} {n.item.value:<15.2f} {n.one_d_ing_value:<25.2f} {n.best_ing_value:<20.2f}', file=fout)
        print(f'     {n.item.value - n.cost:<15.2f} {n.item.value - n.one_d_ing_value:<15.2f} {n.item.value-n.best_ing_value:<25.2f}', file=fout)

# -----------------

def outputValueTable(nodes, fout=sys.stdout):
    node_class.Node.topologicalWalk(nodes, calValueTable)
    printValueTable(nodes, fout)
    