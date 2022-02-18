import itertools as itt

class VariableInfo:
    def __init__(self, name, vtype):
        self.name = name
        self.type = vtype
    
    def __str__(self):
        return self.name + ' : ' + self.type.name + '\n'

class Scope:
    def __init__(self, parent=None):
        self.locals = []
        self.children = []
        self.parent = parent
        self.index = 0 if parent is None else len(parent)

    def __len__(self):
        return len(self.locals)

    def create_child(self):
        child = Scope(self)
        self.children.append(child)
        return child

    def define_variable(self, vname, vtype):
        info = VariableInfo(vname, vtype)
        self.locals.append(info)
        return info

    def find_variable(self, vname, scope_class, current_type, index=None):
        locals = self.locals if index is None else itt.islice(self.locals, index)
        try:
            return next(x for x in locals if x.name == vname)
        except StopIteration:
            variable = self.parent.find_variable(vname, scope_class, current_type, self.index) if self.parent is not None else None
            if variable is None and current_type.parent != None and current_type.parent.name != 'Object':
                variable = scope_class[current_type.parent.name].find_variable(vname, scope_class, current_type.parent)
            return variable

    def is_defined(self, vname, scope_class, current_type):
        return self.find_variable(vname, scope_class, current_type) is not None

    def is_local(self, vname):
        return any(True for x in self.locals if x.name == vname)