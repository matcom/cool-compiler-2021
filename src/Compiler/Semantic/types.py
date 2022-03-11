class COOL_Type:
    
    def __init__(self, name, parent = None):
        self.name = name
        self.parent = parent
        self.attr = dict()
        self.func = dict()
    
    def add_func(self, name, func):
        if not self.func.get(name) is None:
            return False
        current = self.parent
        while not current is None:
            if not current.func.get(name) is None:
                _function = current.func[name]
                if list(_function['formal_params'].values()) != list(func['formal_params'].values()):
                    return None
                if _function['return_type'] != func['return_type']:
                    return None
                self.func[name] = func
                return True
            current = current.parent
        self.func[name] = func
        return True
    
    def add_funcs(self, funcs):
        result = True
        for (name, func) in funcs:
            result &= self.add_func(name, func)
        return result
    
    def add_attr(self, name, _type, expr = None):
        if not self.attr.get(name) is None:
            return False
        current = self.parent
        while not current is None:
            if not current.attr.get(name) is None:
                return None
            current = current.parent
        self.attr[name] = {'expresion': expr, 'type': _type}
        return True
    
    def get_func(self, name):
        current = self
        while not current is None:
            if not current.func.get(name) is None:
                return current.func[name]
            current = current.parent
        return None
    
    def get_func_context(self, name):
        current = self
        while not current is None:
            if not current.func.get(name) is None:
                return current
            current = current.parent
        return None
    
    def get_all_parents(self):
        parents = list()
        current = self.parent
        while not current is None:
            parents.append(current)
            current = current.parent
        return parents
    
    def get_attr_type(self, name):
        current = self
        while not current is None:
            if not current.attr.get(name) is None:
                return current.attr[name]['type']
            current = current.parent
        return None
    
    def get_all_attr(self):
        attr = list()
        current = self
        while not current is None:
            attr += list(current.attr.keys())[::-1]
            current = current.parent
        return attr[::-1]

    def get_all_func(self):
        return list(self.func.keys())
    
    def __str__(self):
        return self.name
    
    def __eq__(type1, type2):
        return str(type1) == str(type2)
    
    def __lt__(type1, type2):
        if type1.parent is None:
            return False
        if type1.parent == type2:
            return True
        return type1.parent < type2
    
    def __le__(type1, type2):
        if type1 == type2 or type1 < type2:
            return True
        return False
    
    def __gt__(type1, type2):
        if type2.parent is None:
            return False
        if type2.parent == type1:
            return True
        return type1 > type2.parent
    
    def __ge__(type1, type2):
        if type1 == type2 or type1 < type2:
            return True
        return False


class cool_type:
    
    def __init__(self):
    
        self.OBJECT = COOL_Type("Object")
        self.SELF = COOL_Type("SELF_TYPE")
        self.VOID = COOL_Type("Void", self.OBJECT)
        self.INT = COOL_Type("Int", self.OBJECT)
        self.BOOL = COOL_Type("Bool", self.OBJECT)
        self.STRING = COOL_Type("String", self.OBJECT)
        self.IO = COOL_Type("IO", self.OBJECT)
        self.IO.add_funcs([
            ('out_string', {'formal_params': {'x_1': self.STRING}, 'return_type': self.SELF}),
            ('out_int',    {'formal_params': {'x_1': self.INT},    'return_type': self.SELF}),
            ('in_string',  {'formal_params': {},                   'return_type': self.STRING}),
            ('in_int',     {'formal_params': {},                   'return_type': self.INT})
        ])
        self.OBJECT.add_funcs([
            ('type_name', {'formal_params': {}, 'return_type': self.STRING}),
            ('copy',      {'formal_params': {}, 'return_type': self.SELF}),
            ('abort',     {'formal_params': {}, 'return_type': self.OBJECT})
        ])
        self.STRING.add_funcs([
            ('length', {'formal_params': {},                                 'return_type': self.INT}),
            ('concat', {'formal_params': {'x_1': self.STRING},               'return_type': self.STRING}),
            ('substr', {'formal_params': {'x_1': self.INT, 'x_2': self.INT}, 'return_type': self.STRING})
        ])
        
        self.not_inherits_type = [self.INT, self.BOOL, self.STRING]
        
        self.defined_types = {
            "Object": self.OBJECT,
            "SELF_TYPE": self.SELF,
            "Void": self.VOID,
            "Int": self.INT,
            "Bool": self.BOOL,
            "String": self.STRING,
            "IO": self.IO
        }
        
        self.basic_types = self.defined_types.copy()

def cyclic_inheritance(_type):
    current = _type
    while not current is None:
        current = current.parent
        if current == _type:
            return True
    return False