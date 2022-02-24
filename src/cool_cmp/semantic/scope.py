from cmp.semantic import Scope as DeprecatedScope
from cool.errors.errors import SemanticError
from cool.visitors.visitors import RunVisitor
class Scope(DeprecatedScope):
    
    def __init__(self, parent=None, typex=None):
        super().__init__(parent)
        self.type = typex
    
    def set_parent(self, parent):
        self.parent = parent
        self.index = len(parent.locals)
    
    def set_variable_value(self,name:str,value):
        variable = self.find_variable(name)
        variable.value = value
    
    def find_variable(self, vname, index=None):
        var = super().find_variable(vname, index)
        if var: return var
        try:
            if self.type:
                attribute = self.type.get_attribute(vname)
                return attribute
            return None
        except SemanticError:
            return None
        
    def create_child(self, typex=None):
        child = super().create_child()
        child.type = self.type if not typex else typex
        return child
    
    def get_variable_value(self,name:str):
        variable = self.find_variable(name)
        if hasattr(variable,'value'):
            return variable.value
        else:
            raise TypeError(f"Value of variable {name} is not assigned")

    def instance_copy(self,typex,context,operator,errors):
        scope = Scope(self.parent, self.type)
        scope.index = self.index
        scope.define_variable('self',typex)
        attributes = typex.all_attributes()
        run = RunVisitor(context,scope,operator,errors)
        for var,attr_typex in attributes:
            if var.type.name == 'SELF_TYPE':
                scope.define_variable(var.name,typex)
            else:
                scope.define_variable(var.name,var.type)
        for var,attr_typex in attributes:
            default_node = var.node.expr
            value = run.visit(default_node,scope)
            scope.set_variable_value(var.name,value)
        scope.children = self.children.copy()
        return scope
    
    def copy(self):
        copy_self = Scope(self.parent, self.type)
        copy_self.index = self.index
        copy_self.children = self.children.copy()
        
        for var_info in self.locals:
            var = copy_self.define_variable(var_info.name,var_info.type)
            if hasattr(var_info,'value'):
                var.value = var_info.value.copy()
                
        return copy_self
    
    def _depth(self) -> int:
        if self.parent == None:
            return 0
        else:
            return self.parent._depth() + 1
    
    def __str__(self):
        tab = "    "
        base = tab*self._depth()
        value = base + "Scope: Index->%d\n" % self.index  
        
        base += tab
        
        if self.locals:
            value += base + "Local Variables \n"
            for x in self.locals:
                value += base + tab + x.name + ":" + x.type.name + "\n"
        
        if self.children:
            value += base + "Childrens \n"
            
            for x in self.children:
                value += str(x)
            
        return value
        