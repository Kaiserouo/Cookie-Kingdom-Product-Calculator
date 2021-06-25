from src.utils.ingredient_class import *
from src.utils import product_encoder
from src.utils import node_class

from src.scripts.base_ingr import *
from src.scripts.value import *

if __name__ == '__main__':
    # read in all data
    base_list, compound_list, factory_list = \
        product_encoder.decode('./product_info/products_score.txt')

    # make nodes
    node_dict = node_class.makeNodes(base_list + compound_list)
    nodes = list(node_dict.values())

    factory_node_list = node_class.makeFactoryNodeList(node_dict, factory_list)

    node_class.Node.topologicalWalk(nodes, calBaseComponent)
    for factory_name, node_ls in factory_node_list:
        print(factory_name)
        for node in node_ls:
            print('    ' + node.item.name)
            item_ls = [p for p in node.d.items() if p[1] != 0]
            for i, (ing_name, cnt) in enumerate(item_ls):
                if i == len(item_ls) - 1:
                    print(f'        └── {ing_name}:{cnt}')
                else:
                    print(f'        ├── {ing_name}:{cnt}')
                    

# if __name__ == '__main__':
#     # read in all data
#     base_list, compound_list = product_encoder.decode('product_info/products.txt')

#     # make nodes
#     node_dict = node_class.make_nodes(base_list, compound_list)
#     nodes = list(node_dict.values())

#     # walk
#     with open('result/base_ingr.txt', 'w') as fout:
#         outputBaseIngredients(nodes, fout)

#     with open('result/craft_tree_minimal.txt', 'w') as fout:
#         outputCraftTree(nodes, fout, minimal=True)

#     with open('result/craft_tree.txt', 'w') as fout:
#         outputCraftTree(nodes, fout, minimal=False)

#     with open('result/value_table.txt', 'w') as fout:
#         outputValueTable(nodes, fout)
