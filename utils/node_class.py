from .ingredient_class import *
import functools
import itertools

class Node:
    """
        simple DAG graph node
    """
    def __init__(self, item):
        self.in_nodes = set()
        self.out_nodes = set()
        self.in_req_amt = dict()
        self.item = item
        item.node = self

    def connectLink(self, to_node, req_amt=1):
        # make link (self -> to_node)
        self.out_nodes.add(to_node)
        to_node.in_nodes.add(self)
        to_node.in_req_amt[self] = req_amt
    
    def deleteLink(self, to_node):
        # delete link (self -> to_node)
        self.out_nodes.remove(to_node)
        to_node.in_nodes.remove(self)
    
    def getReqAmt(self, ing_node):
        # get required amount for an ingredient
        return self.in_req_amt[ing_node] if ing_node in self.in_req_amt else None
    
    # in / out degree of this node. Note that it doesn't have to do
    # with cur_in_deg in topologicalWalk.
    @property
    def in_deg(self):
        return len(self.in_nodes)
    @property
    def out_deg(self):
        return len(self.out_nodes)
    
    @functools.total_ordering
    def __lt__(self, other):
        # compares with other node
        return self.item < other.item
    
    @staticmethod
    def topologicalWalk(nodes, apply_func):
        # apply `apply_func` to nodes in the order of topological sort.
        # nodes: List[Nodes]
        avail_nodes = [node for node in nodes if node.in_deg == 0]
        for node in nodes: 
            node.cur_in_deg = node.in_deg
        while len(avail_nodes) != 0:
            cur_node = avail_nodes[0]
            apply_func(cur_node)
            for to_node in cur_node.out_nodes:
                to_node.cur_in_deg -= 1
                if to_node.cur_in_deg == 0:
                    avail_nodes.append(to_node)
            avail_nodes.pop(0)

    def __str__(self):
        return str(self.item)
    def __repr__(self):
        return str(self.item)

def make_nodes(*ing_lists):
    # List[Union[Base, Compound]], ... -> Map[Name: Node]
    node_dict = {
        ing.name: Node(ing) 
        for ing in itertools.chain.from_iterable(ing_lists)
    }

    for node in node_dict.values():
        if isinstance(node.item, Compound):
            # let its parent ingredients link to self
            for p in node.item.ingredients:
                ing_name = p[0]
                node_dict[ing_name].connectLink(node, p[1])
    
    return node_dict