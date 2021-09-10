class Node:
    pass 

class ProgramNode (Node): 
    def __init__(self, types, data, code):
        self.types = types
        self.data = data
        self.code = code

    def __str__(self):
        types = ''
        data = ''
        code = ''

        for t in self.types:
            types += str(t)
        for d in self.data:
            data += str(d)
        for c in self.code:
            code += str(c)

        return f'.TYPES\n\n{types}\n.DATA\n\n{data}\n.CODE\n\n{code}'

class TypesNode (Node):  
    def __init__(self, id, attrubutes, methodos):
        self.id = id
        self.methods = methodos
        self.attributes = attrubutes

    def __str__(self):
        attr = ''
        meth = ''
        
        for a in self.attributes:
            attr += f'\tattribute {a} ;'
        for m in self.methods:
            meth += f'\tmethod {m[0]}:{m[1]}_{m[0]} ;'

        return f'type {self.id} {{\n{attr}\n{meth}}}\n'

class CodeNode (Node):  
    def __init__(self, id, params, locals, functions):
        self.id = id
        self.params = params
        self.locals = locals
        self.functions = functions

    def __str__(self):
        local = ''
        params = ''
        functions = ''
        
        for p in self.params:
            params += f'\t{p}'
        for l in self.locals:
            local += f'\t{l}'
        for f in self.functions:
            functions += f'\t{f}'
        
        return f'function {self.id} {{\n{params}{local}{functions}}}'
        

class LocalNode (Node):  
    def __init__(self, id):
        self.id = id
    
    def __str__(self):
        return f'{self.id} ;'

class ParamNode (Node):  
    def __init__(self, id):
        pass
    
    def __str__(self): 
        return f'PARAM {self.id} ;'

class InstructionNode (Node):  
    def __init__(self, value_1, value_2, value_3):
        self.value_1 = value_1
        self.value_2 = value_2
        self.value_3 = value_3

class Assignment (InstructionNode): 
    def __str__(self): 
        return f'{self.value_1} = {self.value_2} ;'

class GetAttributeNode (InstructionNode): 
    def __str__(self): 
        return f'{{self.value_1}} = GETATTR {self.value_2} {self.value_3} ;'

class SetAttributeNode (InstructionNode): 
    def __str__(self): 
        return f'SETATTR {self.value_1} {self.value_2} {self.value_3} ;'

class GetIndexNode (InstructionNode): 
    def __str__(self): 
        return f'{self.value_1} = GETINDEX {self.value_2} {self.value_3} ;'

class SetIndexNode (InstructionNode): 
    def __str__(self): 
        return f'SETINDEX {self.value_1} {self.value_2} {self.value_3} ;'

class AllocateNode (InstructionNode): 
    def __str__(self): 
        return f'{self.value_1} = ALLOCATE {self.value_2} ;'

class ArrayNode (InstructionNode): 
    def __str__(self): 
        return f'{self.value_1} = ARRAY {self.value_2} ;'

class TypeOfNode (InstructionNode): 
    def __str__(self): 
        return f'{self.value_1} = TYPEOF {self.value_2}'

class LabelNode (InstructionNode): 
    def __str__(self): 
        return f'LABEL {self.value_1} ;'

class GotoNode (InstructionNode): 
    def __str__(self): 
        return f'GOTO {self.value_1} ;'

class ConditionalNode (InstructionNode): 
    def __str__(self): 
        return f'IF {self.value_1} GOTO {self.value_1} ;'

class StaticCallNode (InstructionNode): 
    def __str__(self): 
        return f'{self.value_1} = CALL {self.value_2} ;'

class DynamicCallNode (InstructionNode): 
    def __str__(self): 
        return f'{self.value_1} = VCALL {self.value_2} {self.value_3}'

class ArgumentNode (InstructionNode): 
    def __str__(self): 
        return f'ARG {self.value_1} ;'

class ReturnNode (InstructionNode): 
    def __str__(self): 
        return f'RETURN {self.value_1} ;'

class LoadAddressNode (InstructionNode): 
    def __str__(self): 
        return f'{self.value_1} = LOAD {self.value_2} ;'

class LengthNode (InstructionNode): 
    def __str__(self): 
        return f'{self.value_1} = LENGTH {self.value_2} ;'

class ConcatNode (InstructionNode): 
    def __str__(self): 
        return f'{self.value_1} = CONCAT {self.value_2} {self.value_3} ;'

class PrefixNode (InstructionNode): 
    def __str__(self): 
        return f'{self.value_1} = PREFIX {self.value_2} {self.value_3} ;'

class SubStringNode (InstructionNode): 
    def __str__(self): 
        return f'{self.value_1} = SUBSTRING {self.value_2} {self.value_3} ;'

class CastStringNode (InstructionNode): 
    def __str__(self): 
        return f'{self.value_1} = STR {self.value_2} ;'

class ReadNode (InstructionNode): 
    def __str__(self): 
        return f'{self.value_1} = READ ;'

class PrintNode (InstructionNode): 
    def __str__(self): 
        return f'PRINT {self.value_1} ;'

class BinaryNode (InstructionNode): 
    pass

class PlusNode (BinaryNode): 
    def __str__(self): 
        return f'{self.value_1} = {self.value_2} + {self.value_3} ;'

class MinusNode (BinaryNode): 
    def __str__(self): 
        return f'{self.value_1} = {self.value_2} - {self.value_3} ;'

class StarNode (BinaryNode): 
    def __str__(self): 
        return f'{self.value_1} = {self.value_2} * {self.value_3} ;'

class DivideNode (BinaryNode): 
    def __str__(self): 
        return f'{self.value_1} = {self.value_2} / {self.value_3} ;'

class LessEqual (BinaryNode): 
    def __str__(self): 
        return f'{self.value_1} = {self.value_2} <= {self.value_3} ;'

class LessNode (BinaryNode): 
    def __str__(self): 
        return f'{self.value_1} = {self.value_2} < {self.value_3} ;'