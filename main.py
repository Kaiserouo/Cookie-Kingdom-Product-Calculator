from ingredient_class import *
import product_encoder
import node_class

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
    
def printValueTable(nodes):
    print("""\
cost: ingredient cost of making it
    i.e. sum of all base ingredient cost needed
one_d_ing_value: sum of sell value of ingredients
                 i.e. one-depth best ingredient value search
best_value: best possible selling value of ingredients
""")
    print(f'     ing_cost(ic)    value           one_d_ing_value(odiv)     best_ing_value(biv)')
    print(f'     value-ic        value-odiv      value-biv')
    print(f'-------------------------------------------------------------------------------------------')
    for n in nodes:
        print(f'{n.item.name}\n     {n.cost:<15.2f} {n.item.value:<15.2f} {n.one_d_ing_value:<25.2f} {n.best_ing_value:<20.2f}')
        print(f'     {n.item.value - n.cost:<15.2f} {n.item.value - n.one_d_ing_value:<15.2f} {n.item.value-n.best_ing_value:<25.2f}')

# --------------

def calBaseComponent(node):
    def dictAdd(d1, d2, mul):
        for p in d2.items():
            d1[p[0]] += p[1] * mul

    d = {
        '瑞士卷木柴': 0, '豆豆果凍': 0, '方糖': 0,
        '餅乾粉': 0, '果凍莓': 0, '香醇牛奶': 0, '棉花糖羊毛': 0
    }
    if isinstance(node.item, Base):
        d[node.item.name] = 1
    else:
        for n in node.in_nodes:
            dictAdd(d, n.d, node.getReqAmt(n))
    node.d = d

def printBaseComponent(nodes):
    for n in nodes:
        print(f"{n.item.name}: ", end='')
        for i in n.d.items():
            print(f'{i[0]}:{i[1]} ', end='')
        print()

if __name__ == '__main__':
    # read in all data
    base_list, compound_list = product_encoder.decode('products.txt')

    # make nodes
    node_dict = node_class.make_nodes(base_list, compound_list)
    nodes = list(node_dict.values())

    # walk

    # get all number of base ingredient needed for each product:
    node_class.Node.topologicalWalk(nodes, calBaseComponent)
    printBaseComponent(nodes)
    
    # get all kinds of values for products
    # node_class.Node.topologicalWalk(nodes, calValueTable)
    # printValueTable(nodes)