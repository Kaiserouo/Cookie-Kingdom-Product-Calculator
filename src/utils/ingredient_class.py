import functools
from typing import *

class Base:
    def __init__(self, name, produce_cost, produce_time, value, produce_count=1):
        self.name = name
        self.cost = produce_cost / produce_count        # per one thing
        self.time = produce_time / produce_count        # seconds
        self.value = value
    def __str__(self):
        return f'Base({self.name}, {self.cost}, {self.time}, {self.value})'
    def __repr__(self):
        return self.__str__()

    @functools.total_ordering
    def __lt__(self, other):
        return str(self) < str(other)

class Compound:
    def __init__(self, name, ingredients, value, time):
        self.name = name
        self.ingredients = ingredients  # [(name, count), ...]
                                        # guarentee DAG: has valid topologival sort
        self.time = time                # seconds
        self.value = value
    def __str__(self):
        return f'Compound({self.name}, {self.time}, {self.value}, {self.ingredients})'
    def __repr__(self):
        return self.__str__()
    
    @functools.total_ordering
    def __lt__(self, other):
        return str(self) < str(other)

Product = Union[Base, Compound]

def check_name(base_list: List[Base], compound_list: List[Compound]):
    # check if all names are valid
    # i.e. see whether there are ingredients that are not listed below
    from itertools import chain
    names = set()
    for i in chain(base_list, compound_list):
        names.add(i.name)
    for i in compound_list:
        for j in i.ingredients:
            if j[0] not in names:
                print(str(i))