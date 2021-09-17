class ClassInstance:
    def __init__(self,typex, context, operator, errors,**kwargs):
        self.type = typex
        self.context = context
        self.operator = operator
        self.errors = errors
        self.scope = typex.class_node.scope.instance_copy(typex,context,operator,errors)
        self.scope.set_variable_value('self',self)
        if 'value' in kwargs:
            self.value = kwargs['value']

    def __eq__(self, other):
        if self.type.name == "Void" and other.type.name == "Void":
            return True
        else:
            return super().__eq__(other)
    
    def __hash__(self):
        if self.type.name == "Void":
            return 0
        else:
            return super().__hash__()
    
    def copy(self):
        if hasattr(self,'value'):
            instance = ClassInstance(self.type,self.context,self.operator,self.errors,value=self.value)
        else:
            instance = ClassInstance(self.type,self.context,self.operator,self.errors)
        instance.scope = self.scope.copy()
        return instance
    
    def shallow_copy(self):
        if hasattr(self,'value'):
            instance = ClassInstance(self.type,self.context,self.operator,self.errors,value=self.value)
        else:
            instance = ClassInstance(self.type,self.context,self.operator,self.errors)
        instance.scope.locals = []
        for var_info in self.scope.locals:
            var = instance.scope.define_variable(var_info.name,var_info.type)
            if hasattr(var_info,'value'):
                if hasattr(var_info.value,'value'):
                    var.value = ClassInstance(var_info.value.type,var_info.value.context,var_info.value.operator,var_info.value.errors,value=var_info.value.value)
                else:
                    var.value = var_info.value
        return instance
    
    def __str__(self):
        if hasattr(self,'value'):
            return f'{self.value}: {self.type.name}'
        return f'{self.type.name} instance'