class Node:
    pass

class ProgramNode(Node):
    def __init__(self, types, data, code):
        self.types = types
        self.data = data
        self.code = code

    def __str__(self):
        type_text = ''
        for type in self.types:
            type_text += f'{type}\n'
        
        data_text = ''
        for data in self.data:
            data_text += f'{data}\n'

        code_text = ''
        for code in self.code:
            code_text += f'{code}\n'

        return f'.TYPE\n\n{type_text}\n.DATA\n\n{data_text}\n.CODE\n\n{code_text}'

class TypeNode(Node):
    def __init__(self, name, attrs, meths):
        self.name = name
        self.attrs = attrs
        self.meths = meths

    def __str__(self):
        attr_text = ''
        for attr in self.attrs:
            attr_text += str(attr)
        
        meth_text = ''
        for meth in self.meths:
            meth_text += f'\tmethod {str(meth)} ;\n'

        return f'type {self.name}{{\n{attr_text}{meth_text}}}'

class MethodNode(Node):
    def __init__(self, name, type=None):
        self.name = name
        self.type = type

    def __str__(self):
        return f'{self.type}.{self.name}' if self.type else self.name

class AttributeNode(Node):
    def __init__(self, name, type):
        self.name = name 
        self.type = type

    def __str__(self):
        return f'\tattribute {self.name} ;\n'

class DataNode(Node):
    def __init__(self, id, value):
        self.id = id
        self.value = value

    def __str__(self):
        return f'{self.id} = "{self.value}" ;\n'

class CodeNode(Node):
    def __init__(self, meth, params, locals, instrs):
        self.meth = meth
        self.params = params
        self.locals = locals
        self.instrs = instrs

    def __str__(self):
        params_text = ''
        for param in self.params:
            params_text += f'\tPARAM {param} ;\n'
        
        local_text = ''
        for local in self.locals:
            local_text += f'\tLOCAL {local} ;\n'

        instr_text = ''
        for instr in self.instrs:
            instr_text += f'\t{instr}\n'
        
        return f'function {self.meth} {{\n{params_text}{local_text}{instr_text}}}'

class LocalNode(Node):
    def __init__(self, id):
        self.id = id

    def __str__(self):
        return f'{self.id}'

class ParamNode(Node):
    def __init__(self, id):
        self.id = id
    
    def __str__(self):
        return f'{self.id}'

class AbortNode(Node):
    def __str__(self):
        return f'ABORT'

class InstructionNode (Node):  
    def __init__(self, value_1, value_2=None, value_3=None):
        self.value_1 = value_1
        self.value_2 = value_2
        self.value_3 = value_3

class AssignmentNode (InstructionNode): 
    def __str__(self): 
        return f'{self.value_1} = {self.value_2} ;'

class GetAttributeNode (InstructionNode): 
    def __str__(self): 
        return f'{self.value_1} = GETATTR {self.value_2} {self.value_3} ;'

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
        return f'IF {self.value_1} GOTO {self.value_2} ;'

class StaticCallNode (InstructionNode): 
    def __str__(self): 
        return f'{self.value_1} = CALL {self.value_2} ;'

class DynamicCallNode (InstructionNode): 
    def __str__(self): 
        return f'{self.value_1} = VCALL {self.value_2} {self.value_3} ;'

class ArgumentNode (InstructionNode): 
    def __str__(self): 
        return f'ARG {self.value_1} ;'

class ReturnNode (InstructionNode): 
    def __str__(self): 
        return f'RETURN {self.value_1} ;' if self.value_1 is not None else f'RETURN ;'

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