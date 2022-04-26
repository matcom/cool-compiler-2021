from Semantic.types import *

class VariableInfo:
    def __init__(self, name, vtype):
        self.name = name
        self.type = vtype

class COOL_Scope:
    
    def __init__(self, name, parent):
        self.ctype = cool_type()
        self.classname = name
        self.parent = parent
        self.children = list()
        self.var = dict()
        self.child_index = 0
        
        if not parent is None:
            self.parent.children.append(self)
            self.ctype = parent.ctype
            
    def next_child(self):
        child = self.children[self.child_index]
        
        self.child_index += 1
        if self.child_index >= len(self.children):
            self.child_index = 0
        
        return child
    
    def set_type(self, name):
        current_scope = self
        while not current_scope is None:
            if not current_scope.ctype.defined_types.get(name) is None:
                return False
            current_scope = current_scope.parent
        new_type = COOL_Type(name)
        self.ctype.defined_types[name] = new_type
        return True
    
    
    def get_type(self, _type):
        if type(_type) is str:
            try:
                return self.get_type(self.ctype.defined_types[_type])
            except:
                return None
        elif type(_type) is COOL_Type:
            return _type
        else:
            return None
    
    def define_new_symbol(self, name, _type, override = False):
        current_scope = self
        while not current_scope.classname is None:
            if not current_scope.var.get(name) is None:
                if not override:
                    return False
                current_scope.var[name] = _type
                return True
            current_scope = current_scope.parent
        self.var[name] = _type
        return True

    def get_symbol_type(self, name):
        current_scope = self
        while not current_scope.classname is None:
            if not current_scope.var.get(name) is None:
                return current_scope.var[name]
            current_scope = current_scope.parent
        return None
    
    def get_var(self, _class, name):
        if name == 'self':
            return self.ctype.SELF
        symbol = self.get_symbol_type(name)
        attr = self.get_type(_class).get_attr_type(name)
        if not symbol is None:
            return symbol
        if not attr is None:
            return attr
        return None
            

    def join(self, type1, type2):
        if type1 <= type2:
            return type2
        if type2 <= type1:
            return type1
        return self.join(type1.parent, type2.parent)