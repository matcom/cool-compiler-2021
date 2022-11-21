class SemanticError(Exception):
    @property
    def text(self):
        return self.args[0]

class Attribute:
    def __init__(self, name, typex):
        self.name = name
        self.type = typex

    def __str__(self):
        return f'[attrib] {self.name} : {self.type.name};'

    def __repr__(self):
        return str(self)

class Method:
    def __init__(self, name, params, return_type):
        self.name = name
        self.params = params
        self.return_type = return_type

    def __str__(self):
        params = ', '.join(f'{n}:{t.name}' for n,t in self.params)
        return f'[method] {self.name}({params}): {self.return_type.name};'

    def __eq__(self, other):
        return other.name == self.name and \
            other.param_types == self.param_types

import inspect
def type_body_def(cls):
    for n, f  in inspect.getmembers(cls, predicate=inspect.ismethod):
        if n == '__init__': continue
        if n in cls.__class__.__dict__: f()
