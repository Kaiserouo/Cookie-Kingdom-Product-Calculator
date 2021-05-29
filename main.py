from utils.ingredient_class import *
import utils.product_encoder as product_encoder
import utils.node_class as node_class

from scripts.base_ingr import *
from scripts.value import *

if __name__ == '__main__':
    # read in all data
    base_list, compound_list = product_encoder.decode('product_info/products.txt')

    # make nodes
    node_dict = node_class.make_nodes(base_list, compound_list)
    nodes = list(node_dict.values())

    
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
