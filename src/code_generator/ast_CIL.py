class CILNode:
    pass


class CILProgramNode(CILNode):
    def __init__(self, types, data, functions) :
        self.types = types
        self.data = data
        self.functions = functions
        
    def __str__(self):
        text = "ProgramNode:\n\n"
        text += "Types:\n"
        for t in self.types:
            text += str(t) + "\n"
        text += "Data:\n"
        for d in self.data:
            text += str(d) + '\n'
        text += "Functions:\n"
        for f in self.functions:
            text += str(f) + '\n'
        return text
        

class CILTypeNode(CILNode):
    def __init__(self, id, attributes, methods):
        self.id = id
        self.attributes = attributes
        self.methods = methods

    def __str__(self):
        text = "TypeNode:\n"
        text += f"id: {self.id}\n"
        text += "Attributes:\n"
        for a in self.attributes:
            text += str(a) + '\n'
        text += "Methods:\n"
        for m in self.methods:
            text += str(m) + '\n'
        return text      
        

class CILDataNode(CILNode):
    def __init__(self, id, text):
        self.id = id
        self.text = text
    
    def __str__(self):
        text = "DataNode:\n"
        text += f"  id: {self.id}\n"
        text += f"  text: {self.text}\n"
        return text


class CILFuncNode(CILNode):
    def __init__(self, id, params, locals, instructions):
        self.id = id
        self.params = params
        self.locals = locals
        self.instructions = instructions
        
    def __str__(self):
        text = "FuncNode:\n"
        text += f"id: {self.id}\n"
        text += f"Params:\n" 
        for p in self.params:
            text += str(p) + '\n'
        text += f"Locals:\n" 
        for l in self.locals:
            text += str(l) + '\n'
        text += f"Instructions:\n" 
        for i in self.instructions:
            text += str(i) + '\n'
        return text      


class CILAttributeNode(CILNode):
    def __init__(self, id ,type):
        self.id = id
        self.type = type
        
    def __str__(self):
        text = "AttributeNode:\n"
        text += f"id: {self.id}\n"
        text += f"type: {self.type}\n"
        return text   


class CILMethodNode(CILNode):
    def __init__(self, id, function_id):
        self.id = id
        self.function_id = function_id
        
    def __str__(self):
        text = "MethodNode:\n"
        text += f"id: {self.id}\n"
        text += f"function_id: {self.function_id}\n"
        return text   


class CILParamNode(CILNode):
    def __init__(self, id, type):
        self.id = id
        self.type = type
        
    def __str__(self):
        text = "ParamNode:\n"
        text += f"id: {self.id}\n"
        text += f"type: {self.type}\n"
        return text   


class CILLocalNode(CILNode):
    def __init__(self, id, type):
        self.id = id 
        self.type = type   
        
    def __repr__(self):
        text = "LocalNode:\n"
        text += f"id: {self.id}\n"
        text += f"type: {self.type}\n"
        return text     


# Instructions
class CILInstructionNode(CILNode):
    pass


class CILAssignNode(CILInstructionNode):
    def __init__(self, id, expr):
        self.id = id
        self.expr = expr

    def __str__(self):
        text = "AssignNode:\n"
        text += f"id: {self.id}\n"
        text += f"expr: {self.expr}\n"
        return text     


class CILSetAttributeNode(CILInstructionNode): 
    def __init__(self, id, type, attr , var):
        self.id = id
        self.type = type
        self.attr = attr
        self.var = var
    
    def __str__(self):
        text = "SetAttrNode:\n"
        text += f"id: {self.id}\n"
        text += f"type: {self.type}\n"
        text += f"att: {self.attr}\n"
        text += f"var: {self.var}\n"
        return text         


class CILArgNode(CILInstructionNode):
    def __init__(self, var):
        self.var = var
        
    def __str__(self):
        text = "ArgNode:\n"
        text += f"var: {self.var}\n"
        return text 
   

class CILIfGotoNode(CILInstructionNode):
    def __init__(self, var, label):
        self.var = var
        self.label = label

    def __str__(self):
        text = "IfGotoNode:\n"
        text += f"var: {self.var}\n"
        text += f"label: {self.label}\n"
        return text 
   

class CILGotoNode(CILInstructionNode):
    def __init__(self, label):
        self.label = label       

    def __str__(self):
        text = "GotoNode:\n"
        text += f"label: {self.label}\n"
        return text 


class CILLabelNode(CILInstructionNode):
    def __init__(self, id):
        self.id = id 

    def __str__(self):
        text = "LabelNode:\n"
        text += f"id: {self.id}\n"
        return text 


class CILReturnNode(CILInstructionNode):
    def __init__(self, var = None):
        self.var = var   
    
    def __str__(self):
        text = "ReturnNode:\n"
        if self.var is not None:
            text += f"var: {self.var}\n"               
        return text                      


# Expressions
class CILExpressionNode(CILNode):
    pass


class CILBinaryOperationNode(CILExpressionNode):
    def __init__(self, left, right):
        self.left = left
        self.right = right
        
    def __str__(self):
        text = "BinaryNode:\n"
        text += f"left: {self.left}\n"
        text += f"right: {self.right}\n"
        return text     
    

class CILGetAttribute(CILExpressionNode):
    def __init__(self, var, type, attr):
        self.var = var
        self.type = type
        self.attr = attr
    
    def __str__(self):
        text = "GetAttrNode:\n"
        text += f"var: {self.var}\n"
        text += f"type: {self.type}\n"
        text += f"att: {self.attr}\n"
        return text             
        

class CILAllocateNode(CILExpressionNode):
    def __init__(self, type):
        self.type = type

    def __str__(self):
        text = "AllocateNode:\n"
        text += f"type: {self.type}\n"
        return text    
        

class CILTypeOfNode(CILExpressionNode):
    def __init__(self, var):
        self.var = var    

    def __str__(self):
        text = "TypeOfNode:\n"
        text += f"var: {self.var}\n"
        return text      


class CILCallNode(CILExpressionNode):
    def __init__(self, func):
        self.func = func  
        
    def __str__(self):
        text = "CallNode:\n"
        text += f"func: {self.func}\n"
        return text   


class CILVCallNode(CILExpressionNode):
    def __init__(self, type,  func):
        self.type = type
        self.func = func 
        
    def __str__(self):
        text = "VCallNode:\n"
        text += f"type: {self.type}\n"
        text += f"func: {self.func}\n"
        return text 


class CILLoadNode(CILExpressionNode):
    def __init__(self, var):
        self.var = var

    def __str__(self):
        text = "LoadNode:\n"
        text += f"var: {self.var}\n"
        return text 


class CILAtomicNode(CILExpressionNode):
    def __init__(self, lex):
        self.lex = lex 
            
    def __str__(self):
        text = "AtomicNode:\n"
        text += f"lex: {self.lex}\n"
        return text     


class CILVariableNode(CILAtomicNode):
    pass     


class CILTypeConstantNode(CILAtomicNode):
    pass               
           

class CILNumberNode(CILAtomicNode):
    pass


# Arithmetic Operations
class CILPlusNode(CILBinaryOperationNode):
    pass


class CILMinusNode(CILBinaryOperationNode):
    pass


class CILStarNode(CILBinaryOperationNode):
    pass


class CILDivNode(CILBinaryOperationNode):
    pass


# Comparison Operations
class CILLessNode(CILBinaryOperationNode):
    pass


class CILElessNode(CILBinaryOperationNode):
    pass  


class CILEqualsNode(CILBinaryOperationNode):
    pass


class CILNotEqualsNode(CILBinaryOperationNode):
    pass
                