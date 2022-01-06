import itertools as itt
from collections import OrderedDict
from utils.errors import SemanticError

import itertools as itt
from collections import OrderedDict


class Attribute:
    def __init__(self, name, typex, index):
        self.name = name
        self.type = typex
        self.index = index

    def __str__(self):
        return f'[attrib] {self.name} : {self.type.name};'

    def __repr__(self):
        return str(self)


class Method:
    def __init__(self, name, param_names, params_types, return_type):
        self.name = name
        self.param_names = param_names
        self.param_types = params_types
        self.return_type = return_type

    def __str__(self):
        params = ', '.join(f'{n}:{t.name}' for n, t in zip(
            self.param_names, self.param_types))
        return f'[method] {self.name}({params}): {self.return_type.name};'

    def __eq__(self, other):
        return other.name == self.name and \
            other.return_type == self.return_type and \
            other.param_types == self.param_types

