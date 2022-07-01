import itertools as itt
from .var import VariableInfo

class Scope:
    def __init__(self, parent=None):
        self.locals = []
        self.cil_locals = {}
        self.parent = parent
        self.children = []
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

    def define_cil_local(self, vname, cilname, vtype = None):
        self.define_variable(vname, vtype)
        self.cil_locals[vname] = cilname
        
    
    def get_cil_local(self, vname):
        if self.cil_locals.__contains__(vname):
            return self.cil_locals[vname]
        else: 
            return None
    
    def find_cil_local(self, vname, index=None):
        locals = self.cil_locals.items() if index is None else itt.islice(self.cil_locals.items(), index)
        try:
            return next(cil_name for name, cil_name in locals if name == vname)
        except StopIteration:
            return self.parent.find_cil_local(vname, self.index) if (self.parent is not None) else None

    def find_variable(self, vname, index=None):
        locals = self.locals if index is None else itt.islice(
            self.locals, index)
        try:
            return next(x for x in locals if x.name == vname)
        except StopIteration:
            return self.parent.find_variable(vname, self.index) if (self.parent is not None) else None

    def is_defined(self, vname):
        return self.find_variable(vname) is not None

    def is_defined_cil_local(self, vname):
        return self.find_cil_local(vname ) is not None

    def is_local(self, vname):
        return any(True for x in self.locals if x.name == vname)

    def remove_local(self, vname):
        self.locals = [local for local in self.locals if local.name != vname]
