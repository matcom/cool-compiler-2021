from CIL.ast import *

def builder_types(context):
    types = {}

    for name in context.types:
        type = context.get_type(name)
        
        attrs = []
        meths = []

        if type.parent is not None:
            parent = type.parent

            while parent is not None:
                for i in range(len(parent.attributes)-1, -1, -1):
                    attrs.insert(0, (parent.attributes[i].name, parent.attributes[i].type))
                for i in range(len(parent.methods)-1, -1, -1):
                    meths.insert(0, (parent.methods[i].name, parent.name))
                parent = parent.parent
        
        for meth in type.methods:
            meths.append((meth.name, name))
        for attr in type.attributes:
            attrs.append((attr.name, attr.type))
        
        types[name] = TypeNode(name, attrs, meths)
    
    return types

def builder_init(self):
    self.locals = {}
    self.local_data = {}
    self.instructions = []
    self.params = [ParamNode('self')]

    for attr in self.current.attributes:
        if attr.expr:
            self.visit(attr.expr)
            self.instructions.append(SetAttributeNode(self.params[0], attr.name, attr.expr.computed_value))

    self.instructions.append(ReturnNode(self.params[0]))
    return CodeNode(f'{self.current.name}', f'init', self.params, self.locals.values(), self.instructions, self.current.parent)

def builder_params(metho):
    params = {'self': ParamNode('self')}
    for param in metho.param_names:
        params[param] = ParamNode(param)
    return params

def builder_main():
    return CodeNode(None, 'main', [], 
    [
        LocalNode('local_0'),
        LocalNode('local_1')
    ],
    [
        AllocateNode('local_0', 'Main'),
        ArgumentNode('local_0'),
        StaticCallNode('local_1', 'main')
    ])