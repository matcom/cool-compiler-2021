from CIL.ast import *

def builder_types(contex):
    types = []

    for name in contex.types:
        methods = []
        attributes = []
        current_type = contex.types[name]
    
        if current_type.parent != None:
            current_parent = current_type.parent
    
            while current_parent != None:
                for i in range(len(current_parent.methods)-1, -1, -1):
                    methods.insert(0, MethodNode(current_parent.methods[i].name, current_parent.name))
                for i in range(len(current_parent.attributes)-1, -1, -1):
                    attributes.insert(0, AttributeNode(current_parent.attributes[i].name, current_parent.attributes[i].type))
                current_parent = current_parent.parent       
    
        for item in current_type.methods:
            methods.append(MethodNode(item.name, name))
        for item in current_type.attributes:
            attributes.append(AttributeNode(item.name, item.type))
    
        types.append(TypeNode(name, attributes, methods))
    
    return types

def builder_basic_functions(self):
    locals = [
        LocalNode('main_add'),
        LocalNode('main_return')
    ]
    Main = MethodNode('main', 'Main') 
    code = [CodeNode(MethodNode('main'), [], locals, 
        [
            AllocateNode(locals[0], 'Main'),
            ArgumentNode(locals[0]),
            DynamicCallNode(locals[1], Main.type, Main),
            ReturnNode(locals[1])
        ])]
    for name in self.context.types:
        current_type = self.context.types[name]    
        
        instructions = []
        params = [ParamNode('self')]
        locals = [LocalNode('local_0')] if current_type.parent else []
        
        if current_type.parent:
            instructions.append(StaticCallNode(locals[0], MethodNode('init', current_type.parent.name)))

        for attribute in current_type.attributes:
            if attribute.expr:
                self.visit(attribute.expr)
                instructions.append(SetAttributeNode(params[0], attribute.name, 3))
        
        instructions.append(ReturnNode(params[0]))
        code.append(CodeNode(MethodNode('init', name), params, locals, instructions))
    
    return code