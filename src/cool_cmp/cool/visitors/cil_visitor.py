import cool.ast.cil_ast as cil
from cool.ast.cool_ast import *
import cmp.visitor as visitor
from cmp.semantic import VariableInfo
from cool.semantic.context import Context
from cool.error.errors import RunError, ZERO_DIVISION, AbortError
from cool.semantic.type import SelfType
from math import floor

class CILPrintVisitor():
    @visitor.on('node')
    def visit(self, node):
        pass

    @visitor.when(cil.ProgramNode)
    def visit(self, node):
        dottypes = '\n'.join(self.visit(t) for t in node.dottypes)
        dotdata = '\n'.join(self.visit(t) for t in node.dotdata)
        dotcode = '\n'.join(self.visit(t) for t in node.dotcode)

        return f'.TYPES\n{dottypes}\n\n.DATA\n{dotdata}\n\n.CODE\n{dotcode}'

    @visitor.when(cil.DataNode)
    def visit(self, node):
        return f"{node.name} = {node.value}"

    @visitor.when(cil.TypeNode)
    def visit(self, node):
        attributes = '\n\t'.join(f'attribute {x}' for x in node.attributes)
        methods = '\n\t'.join(f'method {x}: {y}' for x,y in node.methods)

        return f'type {node.name} {{\n\tparent: {node.parent}\n\t{attributes}\n\n\t{methods}\n}}'

    @visitor.when(cil.FunctionNode)
    def visit(self, node):
        params = '\n\t'.join(self.visit(x) for x in node.params)
        localvars = '\n\t'.join(self.visit(x) for x in node.localvars)
        instructions = '\n\t'.join(self.visit(x) for x in node.instructions)

        return f'function {node.name} {{\n\t{params}\n\n\t{localvars}\n\n\t{instructions}\n}}'

    @visitor.when(cil.ParamNode)
    def visit(self, node):
        return f'PARAM {node.name}'

    @visitor.when(cil.LocalNode)
    def visit(self, node):
        return f'LOCAL {node.name}'

    @visitor.when(cil.AssignNode)
    def visit(self, node):
        return f'{node.dest} = {node.source}'

    @visitor.when(cil.PlusNode)
    def visit(self, node):
        return f'{node.dest} = {node.left} + {node.right}'

    @visitor.when(cil.MinusNode)
    def visit(self, node):
        return f'{node.dest} = {node.left} - {node.right}'

    @visitor.when(cil.StarNode)
    def visit(self, node):
        return f'{node.dest} = {node.left} * {node.right}'

    @visitor.when(cil.DivNode)
    def visit(self, node):
        return f'{node.dest} = {node.left} / {node.right}'

    @visitor.when(cil.AllocateNode)
    def visit(self, node):
        return f'{node.dest} = ALLOCATE {node.type}'

    @visitor.when(cil.TypeOfNode)
    def visit(self, node):
        return f'{node.dest} = TYPEOF {node.obj}'

    @visitor.when(cil.TypeNameNode)
    def visit(self, node):
        return f'{node.dest} = TYPENAME {node.type}'

    @visitor.when(cil.StaticCallNode)
    def visit(self, node):
        return f'{node.dest} = CALL {node.function}'

    @visitor.when(cil.DynamicCallNode)
    def visit(self, node):
        return f'{node.dest} = VCALL {node.type} {node.method}'

    @visitor.when(cil.GetAttribNode)
    def visit(self, node):
        return f'{node.dest} = GETATTR {node.source} {node.attr}'

    @visitor.when(cil.SetAttribNode)
    def visit(self, node:cil.SetAttribNode):
        return f'SETATTR {node.source} {node.attr} {node.value}'

    @visitor.when(cil.ArgNode)
    def visit(self, node):
        return f'ARG {node.name}'
    
    @visitor.when(cil.CommentNode)
    def visit(self, node):
        return f'# {node.string}'

    @visitor.when(cil.ReturnNode)
    def visit(self, node):
        return f'RETURN {node.value if node.value is not None else ""}'
    
    @visitor.when(cil.AbortNode)
    def visit(self, node):
        return f'ABORT'
    
    @visitor.when(cil.CopyNode)
    def visit(self, node):
        return f'{node.result} = COPY {node.instance}'
    
    @visitor.when(cil.LengthNode)
    def visit(self, node):
        return f'{node.dest} = LENGTH {node.string_var}'
    
    @visitor.when(cil.ConcatNode)
    def visit(self, node):
        return f'{node.dest} = CONCAT {node.string1} {node.string2}'

    @visitor.when(cil.SubstringNode)
    def visit(self, node):
        return f'{node.dest} = SUBSTRING {node.string} {node.index} {node.length}'

    @visitor.when(cil.PrintNode)
    def visit(self, node):
        return f'PRINT {node.str_addr}'

    @visitor.when(cil.PrintIntNode)
    def visit(self, node):
        return f'PRINTINT {node.int_addr}'

    @visitor.when(cil.ReadNode)
    def visit(self, node):
        return f'{node.dest} = READ'

    @visitor.when(cil.ReadIntNode)
    def visit(self, node):
        return f'{node.dest} = READINT'

    @visitor.when(cil.LoadNode)
    def visit(self, node:cil.LoadNode):
        return f'{node.dest} = LOAD {node.msg}'
    
    @visitor.when(cil.LabelNode)
    def visit(self, node:cil.LabelNode):
        return f'LABEL {node.label}'
    
    @visitor.when(cil.GotoIfNode)
    def visit(self, node:cil.GotoIfNode):
        return f'IF {node.condition_value} GOTO {node.label}'
    
    @visitor.when(cil.GotoNode)
    def visit(self, node:cil.GotoNode):
        return f'GOTO {node.label}'
    
    @visitor.when(cil.NotNode)
    def visit(self, node:cil.NotNode):
        return f'{node.dest} = NOT {node.value}'
    
    @visitor.when(cil.EqualNode)
    def visit(self, node:cil.EqualNode):
        return f'{node.dest} = EQUAL {node.left} {node.right}'
    
    @visitor.when(cil.ObjEqualNode)
    def visit(self, node:cil.ObjEqualNode):
        return f'{node.dest} = OBJEQUAL {node.left} {node.right}'
    
    @visitor.when(cil.GreaterNode)
    def visit(self, node:cil.GreaterNode):
        return f'{node.dest} = {node.left} > {node.right}'
    
    @visitor.when(cil.LesserNode)
    def visit(self, node:cil.LesserNode):
        return f'{node.dest} = {node.left} < {node.right}'
    
    @visitor.when(cil.VoidNode)
    def visit(self, node:cil.VoidNode):
        return f'{node.dest} = VOID'
    
    @visitor.when(cil.GetFatherNode)
    def visit(self, node:cil.GetFatherNode):
        return f'{node.dest} = FATHER {node.variable}'
    
    @visitor.when(cil.ArrayNode)
    def visit(self, node:cil.ArrayNode):
        return f'{node.dest} = ARRAY {node.type} {node.length}'
    
    @visitor.when(cil.SetIndexNode)
    def visit(self, node:cil.SetIndexNode):
        return f'SETINDEX {node.source} {node.index} {node.value}'
    
    @visitor.when(cil.GetIndexNode)
    def visit(self, node:cil.GetIndexNode):
        return f'{node.dest} = GETINDEX {node.source} {node.index}'
    
    @visitor.when(cil.InitInstance)
    def visit(self, node:cil.InitInstance):
        return ""


class CILRunnerVisitor():
    
    def __init__(self) -> None:
        self.data = {}
        self.types = {}
        self.function = {}
        self.errors = []
    
    def jump_to(self, label):
        return ("jump",label)
    
    def return_value(self, value):
        return ("return", value)
    
    def next_instruction(self):
        return ("next", None)
    
    def get_type(self, typex) -> cil.TypeNode:
        if isinstance(typex, cil.TypeNode):
            return typex

        if isinstance(typex, dict):
            return typex["__type"]
        try:
            if isinstance(typex, cil.TypeNode):
                return typex
            return self.types[typex]
        except KeyError:
            self.raise_error("Type {0} isn't defined", typex)
    
    def get_dynamic_type(self, type_name, caller_fun_scope):
        if type_name[0].isupper(): # Type Name
            typex = self.get_type(type_name)
        else: # Type variable
            typex = self.get_type(caller_fun_scope[type_name])
        return typex
    
    def raise_error(self, message, *args):
        raise RunError(message, *args)
    
    def create_type_instance(self, name):
        typex = self.get_type(name)
        return {
            "__type": typex,
            "__is_type": True,
        }
    
    def get_value(self, source, function_scope):
        value = None
        try:
            value = int(source)
        except ValueError:
            if source in function_scope:
                value = function_scope[source]
            elif source in self.types:
                value = self.create_type_instance(source)
            else:
                self.raise_error("Variable {0} doesn't exist", source)
        return value
    
    def set_value(self, dest, value, function_scope):
        if dest not in function_scope:
            self.raise_error("Variable {0} isn't defined", dest)
        function_scope[dest] = value
    
    def get_value_str(self, source, function_scope, error=None):
        value = self.get_value(source, function_scope)
        if not isinstance(value, str):
            if not error:
                error = f"String expected at {source}"
            self.raise_error(error)
        return value
    
    def get_value_int(self, source, function_scope, error=None):
        value = self.get_value(source, function_scope)
        if not isinstance(value, int):
            if not error:
                error = f"Int expected at {source}"
            self.raise_error(error)
        return value
    
    def binary_node(self, node, function_scope, func):
        left = self.get_value(node.left, function_scope)
        right = self.get_value(node.right, function_scope)
        value = func(left, right)
        self.set_value(node.dest, value, function_scope)
        return self.next_instruction()

    def string_cleaner(self, string):
        semi = string[1:-1]
        temp = []
        escape = False
        for ch in semi:
            if ch == '\\' and not escape:
                escape = True
            elif ch == 'n' and escape:
                temp.append('\n')
                escape = False
            elif ch == 't' and escape:
                temp.append('\t')
                escape = False
            elif ch == 'b' and escape:
                temp.append('\b')
                escape = False
            elif ch == 'f' and escape:
                temp.append('\f')
                escape = False
            elif escape:
                temp.append(ch)
                escape = False
            else:
                temp.append(ch)

        return ''.join(temp)
    
    @visitor.on('node')
    def visit(self, node):
        pass

    @visitor.when(cil.ProgramNode)
    def visit(self, node:cil.ProgramNode):
        for t in node.dottypes + [cil.TypeNode("__Array", None, "__Array", row = -1, column=-1, comment="Array type generated in for running")]:
            self.visit(t)
        for t in node.dotdata:
            self.visit(t)
        for t in node.dotcode:
            self.visit(t)
        try:
            result = self.visit(cil.StaticCallNode("main", "result", row=-1, column=-1), [], {"result":None})
            return result
        except RunError as er:
            # er.text = er.text[10:]
            self.errors.append(er)
            return None

    @visitor.when(cil.DataNode)
    def visit(self, node:cil.DataNode):
        if node.name in self.data:
            self.raise_error("Data {0} already defined")
        self.data[node.name] = self.string_cleaner(node.value)

    @visitor.when(cil.TypeNode)
    def visit(self, node:cil.TypeNode):
        if node.name in self.types:
            self.raise_error("Type {0} already defined", node.name)
        self.types[node.name] = node

    @visitor.when(cil.TypeNameNode)
    def visit(self, node:cil.TypeNameNode, args: list, caller_fun_scope: dict):
        typex = self.get_dynamic_type(node.type, caller_fun_scope)
        if typex.name_data not in self.data:
            self.raise_error(f"Data {typex.name_data} not defined")
        value = self.data[typex.name_data]
        self.set_value(node.dest, value, caller_fun_scope)
        return self.next_instruction()

    @visitor.when(cil.FunctionNode)
    def visit(self, node):
        self.function[node.name] = node
        
    @visitor.when(cil.StaticCallNode)
    def visit(self, node:cil.StaticCallNode, args: list, caller_fun_scope: dict):
        try:
            func_node = self.function[node.function]
        except KeyError:
            self.raise_error("Function {0} doesn't exist", node.function)
        
        fun_scope = {}
        label_dict = {}
        current_args = []
        if len(args) != len(func_node.params):
            self.raise_error("Argument amount {0} doesn't match with params amount {1} at {2}", len(args), len(func_node.params), node.function)
        
        for p in func_node.params:
            self.visit(p, args, fun_scope)
        
        for i,label_node in [(i,x) for i,x in enumerate(func_node.instructions) if isinstance(x, cil.LabelNode)]:
            if label_node.label in label_dict:
                self.raise_error("Repeated label {0} at {1}", label_node.name, node.function)
            label_dict[label_node.label] = i
        
        for local in func_node.localvars:
            self.visit(local, current_args, fun_scope)
        
        i = 0
        while i < len(func_node.instructions):
            instr = func_node.instructions[i]
            action,action_info = self.visit(instr, current_args, fun_scope)
            i+=1
            if action == "jump":
                try:
                    i = label_dict[action_info]
                except KeyError:
                    self.raise_error("Missing label {0} at function {1}", action_info, node.function)   
            if action == "return":
                if isinstance(instr, cil.ReturnNode):
                    self.set_value(node.dest, action_info, caller_fun_scope)
                    return self.return_value(action_info)
                else: # A Function call
                    self.set_value(instr.dest, action_info, fun_scope)
        self.raise_error("Missing return at {0}", node.function)
                    
    @visitor.when(cil.DynamicCallNode)
    def visit(self, node, args: list, caller_fun_scope: dict):
        # typex = args[0]['__type']
        typex = self.get_dynamic_type(node.type, caller_fun_scope)
        try:
            func_name = next(static_name for name, static_name in typex.methods if name == node.method)
        except StopIteration:
            self.raise_error("Type {0} doesn't contains method {1}", node.type, node.method)
        return self.visit(cil.StaticCallNode(func_name, node.dest, row=node.row, column=node.column, comment=node.comment), args, caller_fun_scope)

    @visitor.when(cil.ParamNode)
    def visit(self, node:cil.ParamNode, args: list, caller_fun_scope: dict):
        if node.name in caller_fun_scope:
            self.raise_error("Parameter {0} already defined", node.name)
        value = args.pop(0) # Removes argument from caller's list
        caller_fun_scope[node.name] = value
        return self.next_instruction()

    @visitor.when(cil.LocalNode)
    def visit(self, node:cil.LocalNode, args: list, caller_fun_scope: dict):
        if node.name in caller_fun_scope:
            self.raise_error("Variable {0} already defined", node.name)
        caller_fun_scope[node.name] = None
        return self.next_instruction()

    @visitor.when(cil.AssignNode)
    def visit(self, node:cil.AssignNode, args: list, caller_fun_scope: dict):
        value = self.get_value(node.source, caller_fun_scope)
        self.set_value(node.dest, value, caller_fun_scope)
        return self.next_instruction()

    @visitor.when(cil.PlusNode)
    def visit(self, node, args: list, caller_fun_scope: dict):
        return self.binary_node(node, caller_fun_scope, lambda x,y: x+y)

    @visitor.when(cil.MinusNode)
    def visit(self, node, args: list, caller_fun_scope: dict):
        return self.binary_node(node, caller_fun_scope, lambda x,y: x-y)

    @visitor.when(cil.StarNode)
    def visit(self, node, args: list, caller_fun_scope: dict):
        return self.binary_node(node, caller_fun_scope, lambda x,y: x*y)

    @visitor.when(cil.DivNode)
    def visit(self, node, args: list, caller_fun_scope: dict):
        try:
            return self.binary_node(node, caller_fun_scope, lambda x,y: floor(x/y))
        except ZeroDivisionError:
            self.raise_error(ZERO_DIVISION)
        
    @visitor.when(cil.AllocateNode)
    def visit(self, node, args: list, caller_fun_scope: dict):
        typex = self.get_dynamic_type(node.type, caller_fun_scope)
        
        value = self.create_type_instance(typex.name)
        value["__is_type"] = False
        for attr in typex.attributes:
            value[attr] = None
            
        self.set_value(node.dest, value, caller_fun_scope)
        return self.next_instruction()

    @visitor.when(cil.GetFatherNode)
    def visit(self, node:cil.GetFatherNode, args: list, caller_fun_scope: dict):
        typex = self.get_dynamic_type(node.variable, caller_fun_scope)
        if typex.parent == None:
            value = None
        else:
            value = self.create_type_instance(typex.parent)
            
        self.set_value(node.dest, value, caller_fun_scope)
        return self.next_instruction()
        
    @visitor.when(cil.ArrayNode)
    def visit(self, node:cil.ArrayNode, args: list, caller_fun_scope: dict):
        array_type = self.get_dynamic_type(node.type, caller_fun_scope)
        length = self.get_value_int(node.length, caller_fun_scope)
        value = {
            "__type": self.get_type("__Array"),
            "length": length,
            "items": [None for _ in range(length)]
        }
        self.set_value(node.dest, value, caller_fun_scope)
        return self.next_instruction()
    
    @visitor.when(cil.SetIndexNode)
    def visit(self, node:cil.SetIndexNode, args: list, caller_fun_scope: dict):
        value = self.get_value(node.value, caller_fun_scope)
        array = self.get_value(node.source, caller_fun_scope)
        index = self.get_value_int(node.index, caller_fun_scope)
        try:
            array["items"][index] = value
        except IndexError:
            self.raise_error(f"Index {node.index} Out Of Range at {node.source}")
        return self.next_instruction()
    
    @visitor.when(cil.GetIndexNode)
    def visit(self, node:cil.GetIndexNode, args: list, caller_fun_scope: dict):
        array = self.get_value(node.source, caller_fun_scope)
        index = self.get_value_int(node.index, caller_fun_scope)
        try:
            value = array["items"][index]
            self.set_value(node.dest, value, caller_fun_scope)
        except IndexError:
            self.raise_error(f"Index {node.index} Out Of Range at {node.source}")
            
        return self.next_instruction()

    @visitor.when(cil.TypeOfNode)
    def visit(self, node, args: list, caller_fun_scope: dict):
        # value = node.obj
        # while isinstance(value, str):
        value = self.get_value(node.obj, caller_fun_scope)
        if isinstance(value, bool):
            self.set_value(node.dest, self.create_type_instance("Bool"), caller_fun_scope)
        elif isinstance(value, int):
            self.set_value(node.dest, self.create_type_instance("Int"), caller_fun_scope)
        elif isinstance(value, str):
            self.set_value(node.dest, self.create_type_instance("String"), caller_fun_scope)
        else:
            self.set_value(node.dest, self.create_type_instance(value["__type"].name), caller_fun_scope)
        return self.next_instruction()

    @visitor.when(cil.GetAttribNode)
    def visit(self, node, args: list, caller_fun_scope: dict):
        obj_value = self.get_value(node.source, caller_fun_scope)
        if not obj_value:
            obj_value = self.get_value(node.source, caller_fun_scope)
        try:
            value = obj_value[node.attr]
        except KeyError:
            self.raise_error("Attribute {0} not found at object {1}", node.attr, node.source)
        self.set_value(node.dest, value, caller_fun_scope)
        return self.next_instruction()

    @visitor.when(cil.SetAttribNode)
    def visit(self, node:cil.SetAttribNode, args: list, caller_fun_scope: dict):
        obj_value = self.get_value(node.source, caller_fun_scope)
        if node.attr not in obj_value:
            self.raise_error("Attribute {0} not found at object {1}", node.attr, node.source)
        obj_value[node.attr] = self.get_value(node.value, caller_fun_scope)
        return self.next_instruction()

    @visitor.when(cil.ArgNode)
    def visit(self, node, args: list, caller_fun_scope: dict):
        value = self.get_value(node.name, caller_fun_scope)
        args.append(value)
        return self.next_instruction()

    @visitor.when(cil.CommentNode)
    def visit(self, node, args: list, caller_fun_scope: dict):
        return self.next_instruction()

    @visitor.when(cil.ReturnNode)
    def visit(self, node, args: list, caller_fun_scope: dict):
        if node.value is not None:
            value = self.get_value(node.value, caller_fun_scope)
        else:
            value = None
        return self.return_value(value)
    
    @visitor.when(cil.AbortNode)
    def visit(self, node, args: list, caller_fun_scope: dict):
        try:
            typex = caller_fun_scope['self']['__type'].name
        except:
            analisis = caller_fun_scope['self']
            if isinstance(analisis, str):
                typex = 'String'
            elif isinstance(analisis, bool): # TODO Fix bool's conversion to int in Cil
                typex = 'Bool'
            elif isinstance(analisis, int):
                typex = 'Int'

        raise AbortError(typex)
    
    @visitor.when(cil.CopyNode)
    def visit(self, node, args: list, caller_fun_scope: dict):
        value = self.get_value(node.instance, caller_fun_scope)
        if not isinstance(value, (str, int)):
            value = value.copy()
        self.set_value(node.result, value, caller_fun_scope)
        return self.next_instruction()
    
    @visitor.when(cil.LengthNode)
    def visit(self, node, args: list, caller_fun_scope: dict):
        value = self.get_value_str(node.string_var, caller_fun_scope, "LENGTH operation undefined with non String type")
        self.set_value(node.dest, len(value), caller_fun_scope)
        return self.next_instruction()
    
    @visitor.when(cil.ConcatNode)
    def visit(self, node, args: list, caller_fun_scope: dict):
        error = "CONCAT operation undefined with non String type"
        value1 = self.get_value_str(node.string1, caller_fun_scope, error)
        value2 = self.get_value_str(node.string2, caller_fun_scope, error)
        self.set_value(node.dest, value1 + value2, caller_fun_scope)
        return self.next_instruction()

    @visitor.when(cil.SubstringNode)
    def visit(self, node, args: list, caller_fun_scope: dict):
        error1 = "SUBSTRING operation undefined with non String type"
        error2 = "SUBSTRING operation undefined with non Int index"
        error3 = "SUBSTRING operation undefined with non Int length"
        value1 = self.get_value_str(node.string, caller_fun_scope, error1)
        value2 = self.get_value_int(node.index, caller_fun_scope, error2)
        value3 = self.get_value_int(node.length, caller_fun_scope, error3)
        if value2 > len(value1):
            self.raise_error("SUBSTRING Out of range index")
        if value3 < 0:
            self.raise_error("SUBSTRING Negative length")
        if value2 + value3 > len(value1):
            self.raise_error("SUBSTRING Length too long for operation")
        self.set_value(node.dest, value1[value2:value2+value3], caller_fun_scope)
        return self.next_instruction()

    @visitor.when(cil.PrintNode)
    def visit(self, node, args: list, caller_fun_scope: dict):
        value = self.get_value_str(node.str_addr, caller_fun_scope, "PRINT operation undefined with non String type")
        print(value, end="")
        return self.next_instruction()
    
    @visitor.when(cil.PrintIntNode)
    def visit(self, node, args: list, caller_fun_scope: dict):
        value = self.get_value_int(node.int_addr, caller_fun_scope, "PRINTINT operation undefined with non Int type")
        print(value, end="")
        return self.next_instruction()

    @visitor.when(cil.ReadNode)
    def visit(self, node, args: list, caller_fun_scope: dict):
        value = input()
        self.set_value(node.dest, value, caller_fun_scope)
        return self.next_instruction()

    @visitor.when(cil.ReadIntNode)
    def visit(self, node, args: list, caller_fun_scope: dict):
        value = input()
        try:
            value = int(value)
            self.set_value(node.dest, value, caller_fun_scope)
            return self.next_instruction()
        except ValueError:
            raise RunError(f"Readed value {value} isn't an integer")

    @visitor.when(cil.LoadNode)
    def visit(self, node:cil.LoadNode, args: list, caller_fun_scope: dict):
        try:
            value = self.data[node.msg]
        except KeyError:
            self.raise_error("Data {0} isn't defined", node.msg)
        self.set_value(node.dest, value, caller_fun_scope)
        return self.next_instruction()
    
    @visitor.when(cil.LabelNode)
    def visit(self, node:cil.LabelNode, args: list, caller_fun_scope: dict):
        return self.next_instruction()
    
    @visitor.when(cil.GotoIfNode)
    def visit(self, node:cil.GotoIfNode, args: list, caller_fun_scope: dict):
        value = self.get_value(node.condition_value, caller_fun_scope)
        jump = True
        if isinstance(value, int):
            jump = value != 0
        if value is None:
            jump = False
        if jump:
            return self.jump_to(node.label)
        return self.next_instruction()            
    
    @visitor.when(cil.GotoNode)
    def visit(self, node:cil.GotoNode, args: list, caller_fun_scope: dict):
        return self.jump_to(node.label)
    
    @visitor.when(cil.NotNode)
    def visit(self, node:cil.NotNode, args: list, caller_fun_scope: dict):
        value = self.get_value(node.value, caller_fun_scope)
        self.set_value(node.dest, not bool(value), caller_fun_scope)
        return self.next_instruction()
    
    @visitor.when(cil.EqualNode)
    def visit(self, node:cil.EqualNode, args: list, caller_fun_scope: dict):
        def equal(x,y):
            if isinstance(x, int) and isinstance(y, int):
                return x == y
            if isinstance(x, str) and isinstance(y, str):
                if len(x) == len(y) and len(x) == 0:
                    return True
                if len(x) == 1 and len(y) == 1:
                    return x == y
                self.raise_error("Only character comparation available")
                
            if all(not isinstance(z, (int,str)) for z in [x,y]):
                cmp1 = None
                cmp2 = None
                if x is not None:
                    if x["__is_type"]:
                        cmp1 = x["__type"].name
                    else:
                        self.raise_error("Equal operation cant operate")
                if y is not None:
                    if y["__is_type"]:
                        cmp2 = y["__type"].name
                    else:
                        self.raise_error("Equal operation cant operate")
                return cmp1 == cmp2
            else:
                self.raise_error("OPERATION must have both argument ")
        return self.binary_node(node, caller_fun_scope, equal)
    
    @visitor.when(cil.ObjEqualNode)
    def visit(self, node:cil.ObjEqualNode, args: list, caller_fun_scope: dict):
        def equal(x,y):
            if isinstance(x, int) and isinstance(y, int):
                return x == y
            if isinstance(x, str) and isinstance(y, str):
                return x == y
                
            if all(not isinstance(z, (int,str)) for z in [x,y]):
                cmp1 = None
                cmp2 = None
                if x is not None:
                    if x["__is_type"]:
                        cmp1 = x["__type"].name
                    else:
                        cmp1 = id(x) # Compare by ref
                if y is not None:
                    if y["__is_type"]:
                        cmp2 = y["__type"].name
                    else:
                        cmp2 = id(y) # Compare by ref
                return cmp1 == cmp2
            else:
                self.raise_error("OPERATION must have both argument ")
        return self.binary_node(node, caller_fun_scope, equal)
    
    @visitor.when(cil.GreaterNode)
    def visit(self, node:cil.GreaterNode, args: list, caller_fun_scope: dict):
        return self.binary_node(node, caller_fun_scope, lambda x,y: x>y)
    
    @visitor.when(cil.LesserNode)
    def visit(self, node:cil.LesserNode, args: list, caller_fun_scope: dict):
        return self.binary_node(node, caller_fun_scope, lambda x,y: x<y)
    
    @visitor.when(cil.VoidNode)
    def visit(self, node:cil.VoidNode, args: list, caller_fun_scope: dict):
        self.set_value(node.dest, None, caller_fun_scope)
        return self.next_instruction()

    @visitor.when(cil.InitInstance)
    def visit(self, node:cil.InitInstance, args: list, caller_fun_scope: dict):
        return self.next_instruction()


class COOLToCILVisitor():
    
    def __init__(self, context:Context, errors=[]):
        self.errors = errors
        self.dottypes = []
        self.dotdata = []
        self.dotcode = []
        self.current_type = None
        self.current_method = None
        self.current_function = None
        self.abort_data = None
        self.int_name_data = None
        self.bool_name_data = None
        self.context = context
    
    @property
    def params(self):
        return self.current_function.params
    
    @property
    def localvars(self):
        return self.current_function.localvars
    
    @property
    def labels(self):
        return self.current_function.labels
    
    @property
    def instructions(self):
        return self.current_function.instructions
    
    def register_local(self, vinfo, row, column, comment=None):
        m = min([i+1 for i,s in enumerate(self.current_function.name) if s == "_"],default=len(self.current_function.name)-1)
        vinfo.cil_name = f'local_{self.current_function.name[m:]}_{vinfo.name}_{len(self.localvars)}'
        local_node = cil.LocalNode(vinfo.cil_name, row, column, comment)
        self.localvars.append(local_node)
        return vinfo.cil_name

    def define_internal_local(self, row, column, comment=None):
        vinfo = VariableInfo('internal', None)
        return self.register_local(vinfo, row, column, comment)

    def define_label(self, row, column, comment=None):
        m = min([i+1 for i,s in enumerate(self.current_function.name) if s == "_"],default=len(self.current_function.name)-1)
        name = f'{self.current_function.name[m:]}_label_{len(self.labels)}'
        label_node = cil.LabelNode(name, row, column, comment)
        self.labels.append(label_node)
        return label_node
        
    def register_instruction(self, instruction):
        self.instructions.append(instruction)
        return instruction
    
    def to_init_attr_function_name(self, attr_name, type_name):
        return f'__init_{attr_name}_at_{type_name}' # Prefixed with __ to avoid collisions
    
    def to_init_type_function_name(self, type_name):
        return f"__init_{type_name}_type"
    
    def to_function_name(self, method_name, type_name):
        return f'function_{method_name}_at_{type_name}'
    
    def register_function(self, function_name, row, column, comment=None):
        funcs = [x for x in self.dotcode if isinstance(x, cil.FunctionNode) and x.name == function_name]
        if len(funcs) > 0:
            self.dotcode.remove(funcs[0])

        function_node = cil.FunctionNode(function_name, [], [], [], [],row,column,comment)
        self.dotcode.append(function_node)
        return function_node
    
    def get_function(self, function_name):
        funcs = [x for x in self.dotcode if isinstance(x, cil.FunctionNode) and x.name == function_name]
        return funcs[0]

    def register_type(self, name, parent=None, row=None, column=None, comment=None):
        if parent:
            for t in self.dottypes:
                if t.name == name and ((t.parent and parent.name != t.parent.name) or not t.parent):
                    t.parent = [x for x in self.dottypes if x.name == parent.name][0]
                    return t

            parent = parent.name

        if len([x for x in self.dottypes if x.name == name]) == 0:
            type_name_data_node = self.register_data('"'+name+'"', row, column, comment)
            if name == "Int": # Assign Type name node address for non reference type
                self.int_name_data = type_name_data_node
            elif name == "Bool":
                self.bool_name_data = type_name_data_node
            type_node = cil.TypeNode(name, parent, type_name_data_node.name, row, column, comment)
            self.dottypes.append(type_node)
            return type_node

        else:
            return self.get_dottype(name)

    def get_dottype(self, name):
        return [x for x in self.dottypes if x.name == name][0]

    def register_data(self, value, row, column, comment=None):
        vname = f'data_{len(self.dotdata)}'
        data_node = cil.DataNode(vname, value, row, column, comment)
        self.dotdata.append(data_node)
        return data_node
    
    def create_entry_function(self, row, column, comment=None):
        self.current_function = self.register_function('main', row, column, comment)
        instance = self.define_internal_local(row, column, comment)
        result = self.define_internal_local(row, column, comment)
        main_method_name = self.to_function_name('main', 'Main')
        main_type = self.context.get_type("Main")
        main_node = InstantiateNode(("Main",0,0),0,0)
        instance = self.visit(main_node, main_type.class_node.scope)
        self.register_instruction(cil.ArgNode(instance, row, column))
        self.register_instruction(cil.StaticCallNode(main_method_name, result, row, column, comment))
        self.register_instruction(cil.ReturnNode("0", row, column, comment))
        self.current_function = None
    
    def create_type_distance_function(self, row, column, comment=None):
        self.current_function = self.register_function('type_distance', row, column, comment)
        type1 = "type1"
        type2 = "type2"
        self.params.append(cil.ParamNode(type1, row, column, comment))
        self.params.append(cil.ParamNode(type2, row, column, comment))
        
        start_label = self.define_label(row, column, comment)
        end_label = self.define_label(row, column, comment)
        fail_label = self.define_label(row, column, comment)
        
        index = self.define_internal_local(row, column, comment)
        equal = self.define_internal_local(row, column, comment)
        equal_void = self.define_internal_local(row, column, comment)
        void = self.define_internal_local(row, column, comment)
        self.register_instruction(cil.VoidNode(void, row, column, comment))
        self.register_instruction(cil.AssignNode(index, "0", row, column, comment))
        
        self.register_instruction(start_label)
        self.register_instruction(cil.EqualNode(equal, type1, type2, row, column, comment))
        self.register_instruction(cil.GotoIfNode(equal, end_label.label, row, column, comment))
        self.register_instruction(cil.GetFatherNode(type1, type1, row, column, comment))
        self.register_instruction(cil.EqualNode(equal_void, type1, void, row, column, comment))
        self.register_instruction(cil.GotoIfNode(equal_void, fail_label.label, row, column, comment))
        self.register_instruction(cil.PlusNode(index, index, "1", row, column, comment))
        self.register_instruction(cil.GotoNode(start_label.label, row, column, comment))
        
        self.register_instruction(fail_label)
        self.register_instruction(cil.AssignNode(index, "-1", row, column, comment))
        self.register_instruction(end_label)
        self.register_instruction(cil.ReturnNode(index, row, column, comment))
        
        self.current_function = None

    def create_empty_methods(self, typex, dottype, row, column, comment=None):
        """
        Creates all methods and init methods except the main init method
        """
        if typex.parent:
            self.create_empty_methods(typex.parent, dottype, row, column, comment)
        
        for attr in typex.attributes:
            dottype.attributes.append(attr.name)
            new_function = self.register_function(self.to_init_attr_function_name(attr.name, typex.name), row, column, f"Init {attr.name} at {typex.name}")
            dottype.methods.append((new_function.name, new_function.name))
        
        for m in typex.methods:
            name = self.to_function_name(m.name, typex.name)
            self.register_function(name, row, column, comment)
            temp = [(x, y) for (x, y) in dottype.methods if x == m.name]
            if len(temp) > 0:
                dottype.methods[dottype.methods.index(temp[0])] = (m.name, name)

            elif len([x for (_, x) in dottype.methods if x == name]) == 0:
                dottype.methods.append((m.name, name))
            
    @visitor.on('node')
    def visit(self, node):
        pass
    
    @visitor.when(ProgramNode)
    def visit(self, node, scope):
        ######################################################
        # node.declarations -> [ ClassDeclarationNode ... ]
        ######################################################
        
        self.create_entry_function(node.row,node.column,"Program Node")
        self.create_type_distance_function(node.row,node.column,"Program Node")
        
        for type_name, typex in self.context.types.items(): # Register all types
            if type_name not in ["Error", "Void"]:
                self.register_type(type_name,parent=None ,row=node.row, column=node.column, comment="Program Node")

        for type_name, typex in self.context.types.items(): # Assign parents to types
            if type_name not in ["Error", "Void"]:
                self.register_type(type_name, typex.parent,
                                   node.row, node.column, "Program Node")

        self.abort_data = self.register_data('"Abort called from class "', node.row, node.column, "Register abort message")

        for type_name, typex in self.context.types.items(): # Create methods
            if type_name not in ["Error", "Void"]:
                this_type = next(x for x in self.dottypes if x.name == type_name)
                self.create_empty_methods(typex, this_type, node.row, node.column, "Program Node")

        for type_name, typex in self.context.types.items():
            if type_name in self.context.special_types and type_name not in ["Error", "Void"]:
                self.visit(typex.class_node, typex.class_node.scope)
        
        for declaration, child_scope in zip(node.declarations, scope.children):
            self.visit(declaration, child_scope)

        return cil.ProgramNode(self.dottypes, self.dotdata, self.dotcode, node.row, node.column)
    
    @visitor.when(ClassDeclarationNode)
    def visit(self, node, scope):
        ####################################################################
        # node.id -> str
        # node.parent -> str
        # node.features -> [ FuncDeclarationNode/AttrDeclarationNode ... ]
        ####################################################################
        
        self.current_type = self.context.get_type(node.id)
        
        type_node = self.get_dottype(self.current_type.name)
        
        # Register class init function
        self.current_function = init_function = self.register_function(self.to_init_type_function_name(self.current_type.name), node.row, node.column, "Class Declaration Node")
        type_node.methods.insert(0, ("__init", init_function.name))
        self.params.append(cil.ParamNode('self', node.row, node.column, "Class Declaration Node"))

        if self.current_type.parent and self.current_type.parent.name not in ["String", "Int", "Bool"]:
            self.register_instruction(cil.ArgNode('self', node.row, node.column, "Calling father init function"))
            self.register_instruction(cil.StaticCallNode(self.to_init_type_function_name(self.current_type.parent.name), "self", node.row, node.column))
        
        self.register_instruction(cil.InitInstance('self', type_node.name, node.row, node.column, "Class Declaration Node"))
        
        for attr in self.current_type.attributes:
            # Initializing attribute's init functions
            init_attr_function = self.get_function(self.to_init_attr_function_name(attr.name, type_node.name))
            self.current_function = init_attr_function
            self.visit(attr.node, attr.node.scope)
            
            # Calling function in type init function
            self.current_function = init_function
            dest = self.define_internal_local(row=attr.node.row, column=attr.node.column, comment="Attribute value destination")
            self.register_instruction(cil.ArgNode('self',node.row, node.column, "arg node"))
            self.register_instruction(cil.StaticCallNode(init_attr_function.name, dest, node.row, node.column, "Initialize arg function"))

        self.register_instruction(cil.ReturnNode('self',node.row, node.column, "return node")) # Returning created instance

        
        # Initialize methods
        func_declarations = (f for f in node.features if isinstance(f, FuncDeclarationNode))
        for feature in func_declarations:
            self.current_function = self.get_function(self.to_function_name(feature.id,self.current_type.name))
            self.visit(feature, feature.scope)
                
        self.current_type = None
                
    @visitor.when(FuncDeclarationNode)
    def visit(self, node, scope):
        ###############################
        # node.id -> str
        # node.params -> [ (str, str) ... ]
        # node.type -> str
        # node.body -> [ ExpressionNode ... ]
        ###############################
        
        self.current_method = self.current_type.get_method(node.id, len(node.params))
        
        # Your code here!!! (Handle PARAMS)
        self.params.append(cil.ParamNode('self', node.row, node.column, "Func Declaration Node"))
        for param in self.current_method.param_names:
            self.params.append(cil.ParamNode(param, node.row, node.column, "Func Declaration Node"))

        value = self.visit(node.body, scope)
        
        # Your code here!!! (Handle RETURN)
        self.register_instruction(cil.ReturnNode(value, node.row, node.column, "Func Declaration Node"))
        self.current_method = None

    @visitor.when(AttrDeclarationNode)
    def visit(self, node, scope):
        self.params.append(cil.ParamNode('self', node.row, node.column, "Attr Declaration Node"))
        result = self.visit(node.expr, scope)
        attr_offset = self.current_type.get_attribute_index(node.id, self.current_type)
        self.register_instruction(cil.SetAttribNode("self", node.id, result, attr_offset, node.row, node.column, "Attr Declaration Node"))
        self.register_instruction(cil.ReturnNode(value= None, row= node.row, column= node.column, comment="Attr Declaration Node"))
        return result
    
    @visitor.when(VarDeclarationNode)
    def visit(self, node, scope):
        ###############################
        # node.id -> str
        # node.type -> str
        # node.expr -> ExpressionNode
        ###############################
        # Your code here!!!
        local = scope.find_variable(node.id)
        cil_local = self.register_local(local, node.row, node.column, "Var Declaration Node")
        value = self.visit(node.expr,scope)
        self.register_instruction(cil.AssignNode(cil_local,value,node.row,node.column,"Var Declaration Node"))
        return cil_local

    @visitor.when(AssignNode)
    def visit(self, node, scope):
        ###############################
        # node.id -> str
        # node.expr -> ExpressionNode
        ###############################
        local = scope.find_variable(node.id)
        value = self.visit(node.expr,scope)
        if hasattr(local,'cil_name'):
            self.register_instruction(cil.AssignNode(local.cil_name,value,node.row,node.column, "Assign Node"))
            return local.cil_name
        else:
            if any(x for x in self.params if x.name == local.name):
                self.register_instruction(cil.AssignNode(local.name, value, node.row,node.column, "Assign Node")) # Param
                return local.name
            else:
                attr_offset = self.current_type.get_attribute_index(local.name, self.current_type)
                self.register_instruction(cil.SetAttribNode('self',local.name, value, attr_offset, node.row, node.column, "Assign Node"))
                # value = self.define_internal_local() # Attr
                # self.register_instruction(cil.GetAttribNode('self',local.name,value))
                return value # or self ?

    @visitor.when(CallNode)
    def visit(self, node:CallNode, scope):
        ###############################
        # node.obj -> AtomicNode
        # node.id -> str
        # node.args -> [ ExpressionNode ... ]
        ###############################
        
        obj_value = self.visit(node.obj,scope)

        # Calling static method with no by reference type 
        if node.obj.type.name in ["Int", "Bool"] and not node.at:
            node.at = node.obj.type
        
        args = []
        if node.at:
            method = node.at.get_method(node.id, len(node.args))
        else:
            method = node.obj.type.get_method(node.id, len(node.args))
            
        for arg_node in node.args:
            value = self.visit(arg_node,scope)
            args.append(value)
            
        result = self.define_internal_local(node.row, node.column, comment=f"Result value of function {node.id}")
        
        self.register_instruction(cil.ArgNode(obj_value, node.row, node.column, "Call Node")) # self
        for arg,value in zip(method.param_names,args):
            self.register_instruction(cil.ArgNode(value, node.row, node.column, "Call Node"))   

        defining_type = None
        if node.at:
            if isinstance(node.at, SelfType):
                defining_type = node.at.defining_type
                self.register_instruction(cil.DynamicCallNode(node.at.name, node.id, result, defining_type, node.row, node.column, "Call Node"))
            else:
                type_node = next(x for x in self.dottypes if x.name == node.at.name)
                cil_name = next(cil_name for cool_name, cil_name in type_node.methods if cool_name == node.id)
                self.register_instruction(cil.StaticCallNode(cil_name, result, node.row, node.column, "Call Node"))
        else:
            # if isinstance(node.obj.type, SelfType):
            #     defining_type = node.obj.type.defining_type
            #     self.register_instruction(cil.DynamicCallNode(node.obj.type.name,node.id,result, defining_type))
            # else:
            #     type_node = next(x for x in self.dottypes if x.name == node.obj.type.name)
            #     cil_name = next(cil_name for cool_name, cil_name in type_node.methods if cool_name == node.id)
            #     self.register_instruction(cil.StaticCallNode(cil_name, result))

            if isinstance(node.obj.type, SelfType):
                defining_type = node.obj.type.defining_type
            else:
                defining_type = node.obj.type

            type_var = self.define_internal_local(node.row, node.column, "Call Node")

            self.register_instruction(cil.TypeOfNode(obj_value, type_var, node.row, node.column, "Call Node"))
            
            self.register_instruction(cil.DynamicCallNode(type_var, node.id, result, defining_type, node.row, node.column, "Call Node"))

        return result
    
    @visitor.when(LetNode)
    def visit(self, node:LetNode, scope):
        current_scope = node.scope
        for param in node.params:
            current_scope = current_scope.children[0]
            self.visit(param, current_scope)
        current_scope = current_scope.children[-1]
        result = self.visit(node.expr, current_scope)
        return result            
    
    @visitor.when(CheckNode)
    def visit(self, node:CheckNode, scope, check_value):
        scope = node.scope
        local = scope.find_variable(node.id)
        cil_local = self.register_local(local, node.row, node.column, "Check Node") 
        self.register_instruction(cil.AssignNode(cil_local, check_value, node.row, node.column, "Check Node"))
        result = self.visit(node.expr, scope)
        return result
    
    @visitor.when(CaseNode)
    def visit(self, node: CaseNode, scope):
        
        value = self.visit(node.expr, scope)
        final_result = self.define_internal_local(node.row, node.column, "Case Node local final result")
        
        type_value = self.define_internal_local(node.row, node.column, "Case Node local type value")
        self.register_instruction(cil.TypeOfNode(value, type_value, node.row, node.column, "Case Node typeof value"))
        checks = len(node.params)
        
        array_types = self.define_internal_local(node.row, node.column, "Case Node array types")
        self.register_instruction(cil.ArrayNode(array_types, "Object", checks, node.row, node.column, "Case Node array declaration")) # Type Object because at the end all are Objects
        
        for i,param in enumerate(node.params):
            self.register_instruction(cil.SetIndexNode(array_types, str(i), param.type.name, node.row, node.column, f"Case Node array setindex {i}"))
        
        index = self.define_internal_local( node.row, node.column, "Case Node local index")
        minim_index = self.define_internal_local( node.row, node.column, "Case Node local minim index")
        minim = self.define_internal_local(node.row, node.column, "Case Node local minim")
        distance = self.define_internal_local( node.row, node.column, "Case Node local distance")
        current_type = self.define_internal_local( node.row, node.column, "Case Node local current type")
        self.register_instruction(cil.AssignNode(index, "-1", node.row, node.column, "Case Node assign index -1"))
        self.register_instruction(cil.AssignNode(minim, "-2", node.row, node.column, "Case Node assign minim -2"))
        
        start_label = self.define_label(node.row, node.column, "Case Node start label")
        minim_label = self.define_label( node.row, node.column, "Case Node minim label")
        end_label = self.define_label( node.row, node.column, "Case Node end label")
        abort_label = self.define_label( node.row, node.column, "Case Node abort label")
        stop_for = self.define_internal_local( node.row, node.column, "Case Node local stop_for")
        not_valid_distance = self.define_internal_local( node.row, node.column, "Case Node local not_valid_distance")
        minim_cond = self.define_internal_local( node.row, node.column, "Case Node local minim_cond")
        
        self.register_instruction(start_label)
        self.register_instruction(cil.PlusNode(index, index, "1", node.row, node.column, "Case Node plus index 1"))
        self.register_instruction(cil.EqualNode(stop_for, index, str(checks), node.row, node.column, "Case Node equal stop_for index checks"))
        self.register_instruction(cil.GotoIfNode(stop_for, end_label.label, node.row, node.column, "Case Node gotoif stop_for end_label"))
        
        
        self.register_instruction(cil.GetIndexNode(array_types, index, current_type, node.row, node.column, "Case Node get_index array_types index"))
        
        self.register_instruction(cil.ArgNode(type_value, node.row, node.column, "Case Node arg type_value"))
        self.register_instruction(cil.ArgNode(current_type, node.row, node.column, "Case Node arg current_type"))
        self.register_instruction(cil.StaticCallNode("type_distance", distance, node.row, node.column, "Case Node static_call type_distance"))
        
        self.register_instruction(cil.EqualNode(not_valid_distance, distance, "-1", node.row, node.column, "Case Node equal not_valid_distance distance -1")) 
        self.register_instruction(cil.GotoIfNode(not_valid_distance, start_label.label, node.row, node.column, "Case Node gotoif not_valid_distance start_label"))
        
        self.register_instruction(cil.EqualNode(minim_cond, minim, "-2", node.row, node.column, "Case Node equal minim_cond minim -2"))
        self.register_instruction(cil.GotoIfNode(minim_cond, minim_label.label, node.row, node.column, "Case Node gotoif minim_cond minim_label"))
        self.register_instruction(cil.GreaterNode(minim_cond, minim, distance, node.row, node.column, "Case Node greater minim_cond minim distance"))
        self.register_instruction(cil.GotoIfNode(minim_cond, minim_label.label, node.row, node.column, "Case Node gotoif minim_cond minim_label"))
        self.register_instruction(cil.GotoNode(start_label.label, node.row, node.column, "Case Node goto start_label"))
        
        self.register_instruction(minim_label)
        self.register_instruction(cil.AssignNode(minim, distance, node.row, node.column, "Case Node assign minim distance"))
        self.register_instruction(cil.AssignNode(minim_index, index, node.row, node.column, "Case Node assign minim_index index"))
        
        self.register_instruction(cil.GotoNode(start_label.label, node.row, node.column, "Case Node goto start_label"))
        self.register_instruction(end_label)
        
        self.register_instruction(cil.EqualNode(minim_cond, minim, "-2", node.row, node.column, "Case Node equal minim_cond minim -2"))
        self.register_instruction(cil.GotoIfNode(minim_cond, abort_label.label, node.row, node.column, "Case Node gotoif minim_cond abort_label"))
        
        self.register_instruction(cil.GetIndexNode(array_types, minim_index, current_type, node.row, node.column, "Case Node get_index array_types minim_index"))
        
        final_label = self.define_label( node.row, node.column, "Case Node final_label")
        not_equal_types = self.define_internal_local( node.row, node.column, "Case Node local not_equal_types")
        end_labels = [self.define_label(node.row, node.column,f"Case Node end_label {i}") for i in node.params]
        for lbl, param, child_scope in zip(end_labels, node.params, node.scope.children):
            self.register_instruction(cil.EqualNode(not_equal_types, param.type.name, current_type, node.row, node.column, "Case Node equal not_equal_types param.type.name current_type"))
            self.register_instruction(cil.NotNode(not_equal_types, not_equal_types, node.row, node.column, "Case Node not not_equal_types not_equal_types"))
            self.register_instruction(cil.GotoIfNode(not_equal_types, lbl.label, node.row, node.column, "Case Node gotoif not_equal_types lbl.label"))
            
            result = self.visit(param, child_scope, value)
            self.register_instruction(cil.AssignNode(final_result, result, node.row, node.column, "Case Node assign final_result result"))
            
            self.register_instruction(cil.GotoNode(final_label.label, node.row, node.column, "Case Node goto final_label"))
            self.register_instruction(lbl)
        
        self.register_instruction(abort_label)
        self.register_instruction(cil.AbortNode(node.row, node.column, "Case Node abort"))
        self.register_instruction(final_label)
                
        return final_result
    
    @visitor.when(IsVoidNode)
    def visit(self, node:IsVoidNode, scope):
        result = self.define_internal_local( node.row, node.column, "Is Void Node")
        value = self.visit(node.member, scope)
        if node.member.type.name in ["Int", "Bool"]:
            self.register_instruction(cil.AssignNode(result, 0, node.row, node.col, comment="Non object always not void"))
        else:
            void_value = self.define_internal_local( node.row, node.column, "Is Void Node")
            self.register_instruction(cil.VoidNode(void_value, node.row, node.column, "Is Void Node"))
            self.register_instruction(cil.ObjEqualNode(result, value, void_value, node.row, node.column, "Is Void Node", value_compare=False))
        return result 
    
    @visitor.when(ConditionalNode)
    def visit(self, node:ConditionalNode, scope):
        
        result = self.define_internal_local( node.row, node.column, "Conditional Node")
        condition_value = self.visit(node.condition, scope)
        then_label = self.define_label( node.row, node.column, "Conditional Node")
        end_label = self.define_label(  node.row, node.column, "Conditional Node")
        
        self.register_instruction(cil.GotoIfNode(condition_value, then_label.label, node.row, node.column, "Conditional Node"))
        
        else_value = self.visit(node.else_expr, scope)
        self.register_instruction(cil.AssignNode(result, else_value, node.row, node.column, "Conditional Node"))
        self.register_instruction(cil.GotoNode(end_label.label, node.row, node.column, "Conditional Node"))
        
        self.register_instruction(then_label)
        then_value = self.visit(node.then_expr,scope)
        self.register_instruction(cil.AssignNode(result, then_value, node.row, node.column, "Conditional Node"))
        
        self.register_instruction(end_label)
        return result
        
    @visitor.when(BlockNode)
    def visit(self, node:BlockNode, scope):
        scope = node.scope
        result = self.define_internal_local( node.row, node.column, "Block Node")
        for expr in node.expr_list:
            result = self.visit(expr, scope)
        return result

    @visitor.when(WhileNode)
    def visit(self, node:WhileNode, scope):
        result = self.visit(VoidNode(None), scope)
        start_label = self.define_label( node.row, node.column, "While Node")
        loop_label = self.define_label( node.row, node.column, "While Node")
        end_label = self.define_label( node.row, node.column, "While Node")
        
        self.register_instruction(start_label)
        condition_result = self.visit(node.condition, scope)
        
        self.register_instruction(cil.GotoIfNode(condition_result, loop_label.label, node.row, node.column, "While Node"))
        self.register_instruction(cil.GotoNode(end_label.label, node.row, node.column, "While Node"))
        
        self.register_instruction(loop_label)
        self.visit(node.expr, scope)
        
        self.register_instruction(cil.GotoNode(start_label.label, node.row, node.column, "While Node"))
        self.register_instruction(end_label)
        
        return result
    
    @visitor.when(NotNode)
    def visit(self, node, scope):
        result = self.define_internal_local( node.row, node.column, "Not Node")
        value = self.visit(node.member, scope)
        self.register_instruction(cil.NotNode(result, value, node.row, node.column, "Not Node"))
        return result
    
    @visitor.when(RoofNode)
    def visit(self, node:RoofNode, scope):
        result = self.define_internal_local( node.row, node.column, "Roof Node")
        value = self.visit(node.member, scope)
        self.register_instruction(cil.MinusNode(result, "0", value, node.row, node.column, "Roof Node"))
        return result
    
    @visitor.when(EqualNode)
    def visit(self, node:EqualNode, scope):
        result = self.define_internal_local( node.row, node.column, "Equal Node")
        
        value1 = self.visit(node.left, scope)
        value2 = self.visit(node.right, scope)

        value_types = ["Int", "Bool"]
        value_compare = node.left.type.name in value_types and node.right.type.name in value_types
        
        self.register_instruction(cil.ObjEqualNode(result, value1, value2, node.row, node.column, "Equal Node", value_compare=value_compare))
        
        return result
    
    @visitor.when(GreaterNode)
    def visit(self, node:GreaterNode, scope):
        result = self.define_internal_local( node.row, node.column, "Greater Node")
        
        value1 = self.visit(node.left, scope)
        value2 = self.visit(node.right, scope)

        self.register_instruction(cil.GreaterNode(result, value1, value2, node.row, node.column, "Greater Node"))
        
        return result
    
    @visitor.when(GreaterEqualNode)
    def visit(self, node, scope):
        result = self.define_internal_local( node.row, node.column, "GreaterEqual Node")
        
        value1 = self.visit(node.left, scope)
        value2 = self.visit(node.right, scope)

        self.register_instruction(cil.LesserNode(result, value1, value2, node.row, node.column, "GreaterEqual Node"))
        self.register_instruction(cil.NotNode(result, result, node.row, node.column, "GreaterEqual Node"))
        
        return result
    
    @visitor.when(LesserNode)
    def visit(self, node, scope):
        result = self.define_internal_local( node.row, node.column, "Lesser Node")
        
        value1 = self.visit(node.left, scope)
        value2 = self.visit(node.right, scope)

        self.register_instruction(cil.LesserNode(result, value1, value2, node.row, node.column, "Lesser Node"))
        
        return result

    @visitor.when(LesserEqualNode)
    def visit(self, node, scope):
        result = self.define_internal_local( node.row, node.column, "LesserEqual Node")
        
        value1 = self.visit(node.left, scope)
        value2 = self.visit(node.right, scope)

        self.register_instruction(cil.GreaterNode(result, value1, value2, node.row, node.column, "LesserEqual Node"))
        self.register_instruction(cil.NotNode(result, result, node.row, node.column, "LesserEqual Node"))
        
        return result
    
    @visitor.when(VoidNode)
    def visit(self, node, scope):
        result = self.define_internal_local( node.row, node.column, "Void Node")
        self.register_instruction(cil.VoidNode(result, node.row, node.column, "Void Node"))
        return result

    @visitor.when(BoolNode)
    def visit(self, node, scope):
        ###############################
        # node.lex -> str
        ###############################
        return "0" if node.lex.lower() == "false" else "1"
    
    @visitor.when(ConstantNumNode)
    def visit(self, node, scope):
        ###############################
        # node.lex -> str
        ###############################
        
        return node.lex

    @visitor.when(VariableNode)
    def visit(self, node, scope):
        ###############################
        # node.lex -> str
        ###############################

        # Your code here!!!
        try:
            return scope.find_variable(node.lex).cil_name # is a Local Variable
        except AttributeError:
            if any(x for x in self.params if x.name == node.lex):
                return node.lex # Param
            else:
                attr_offset = self.current_type.get_attribute_index(node.lex, self.current_type)
                value = self.define_internal_local( node.row,node.column,"Variable Node") # Attr
                self.register_instruction(cil.GetAttribNode('self',node.lex, value, attr_offset, node.row, node.column, "Variable Node"))
                return value
        
    @visitor.when(InstantiateNode)
    def visit(self, node, scope):
        ###############################
        # node.lex -> str
        ###############################
        
        # Your code here!!!
        instance = self.define_internal_local( node.row, node.column, "Instantiate Node")
        instance_typex = self.context.get_type(node.lex, current_type = self.current_type)
        if instance_typex.name == "Void":
            self.register_instruction(cil.VoidNode(instance, node.row, node.column, "Instantiate Node"))
        elif instance_typex.name == "SELF_TYPE":
            dynamic_type = self.define_internal_local( node.row, node.column, "Instantiate Node")
            self.register_instruction(cil.TypeOfNode("self", dynamic_type, node.row, node.column, "Instantiate Node"))
            self.register_instruction(cil.AllocateNode(dynamic_type, instance, node.row, node.column, "Instantiate Node"))
            self.register_instruction(cil.ArgNode(instance, node.row, node.column, "Instantiate Node"))
            self.register_instruction(cil.DynamicCallNode(dynamic_type, "__init", instance, instance_typex.defining_type, node.row, node.column, "Instantiate Node"))
        else:
            self.register_instruction(cil.AllocateNode(instance_typex.name, instance, node.row, node.column, "Instantiate Node"))
            self.register_instruction(cil.ArgNode(instance, node.row, node.column, "Instantiate Node"))
            self.register_instruction(cil.StaticCallNode(self.to_init_type_function_name(instance_typex.name), instance, node.row, node.column, "Instantiate Node"))
        return instance
        
    @visitor.when(PlusNode)
    def visit(self, node, scope):
        ###############################
        # node.left -> ExpressionNode
        # node.right -> ExpressionNode
        ###############################
        
        # Your code here!!!
        left = self.visit(node.left,scope)
        right = self.visit(node.right,scope)
        
        value = self.define_internal_local( node.row, node.column, "Plus Node")
        self.register_instruction(cil.PlusNode(value,left,right,node.row,node.column,"Plus Node"))
        return value

    @visitor.when(MinusNode)
    def visit(self, node, scope):
        ###############################
        # node.left -> ExpressionNode
        # node.right -> ExpressionNode
        ###############################
        
        # Your code here!!!
        left = self.visit(node.left,scope)
        right = self.visit(node.right,scope)
        
        value = self.define_internal_local( node.row, node.column, "Minus Node")
        self.register_instruction(cil.MinusNode(value,left,right,node.row,node.column,"Minus Node"))
        return value

    @visitor.when(StarNode)
    def visit(self, node, scope):
        ###############################
        # node.left -> ExpressionNode
        # node.right -> ExpressionNode
        ###############################
        
        # Your code here!!!
        left = self.visit(node.left,scope)
        right = self.visit(node.right,scope)
        
        value = self.define_internal_local( node.row, node.column, "Star Node")
        self.register_instruction(cil.StarNode(value,left,right,node.row,node.column,"Star Node"))
        return value

    @visitor.when(DivNode)
    def visit(self, node, scope):
        ###############################
        # node.left -> ExpressionNode
        # node.right -> ExpressionNode
        ###############################
        
        # Your code here!!!
        left = self.visit(node.left,scope)
        right = self.visit(node.right,scope)
        
        value = self.define_internal_local( node.row, node.column, "Div Node")
        self.register_instruction(cil.DivNode(value,left,right,node.row,node.column,"Div Node"))
        return value
        
    @visitor.when(StringNode)
    def visit(self, node, scope):
        value = self.register_data(node.lex, node.row, node.column, "String Node")
        result = self.define_internal_local( node.row, node.column, "String Node")
        self.register_instruction(cil.LoadNode(result, value.name, node.row, node.column, "String Node"))
        return result
        
    @visitor.when(SpecialNode)
    def visit(self, node, scope=None):
        return self.visit(node.cil_node_type(row=node.row, column=node.column), scope)



    # META INSTRUCTIONS ONLY USED IN CODE
    # TRANSLATION THAT DOESN'T BELONG TO CIL'S
    # INSTRUCTION SET

    @visitor.when(cil.ObjectCopyNode)
    def visit(self, node, scope=None):
        instance = self.params[0]
        result = self.define_internal_local( node.row, node.column, "Object Copy Node")
        self.register_instruction(cil.CopyNode(instance.name, result, node.row, node.column, "Object Copy Node"))
        return result
    
    @visitor.when(cil.ObjectAbortNode)
    def visit(self, node:cil.ObjectAbortNode, scope=None):
        # Abort called from class {self.typex}
        instance = self.params[0]
        type_var = self.define_internal_local(node.row, node.column, "Dynamic type for abort dispatch")
        type_name = self.define_internal_local(node.row, node.column, "Type name address")
        abort_first_msg = self.define_internal_local(node.row, node.column, "First part of the abort message")
        final_msg = self.define_internal_local(node.row, node.column, "Final abort message")

        self.register_instruction(cil.TypeOfNode(instance.name, type_var, node.row, node.column, "Assign object type"))
        self.register_instruction(cil.TypeNameNode(type_var, type_name, node.row, node.column, "Get type name"))
        self.register_instruction(cil.LoadNode(abort_first_msg, self.abort_data.name, node.row, node.column))
        self.register_instruction(cil.ConcatNode(final_msg, abort_first_msg, type_name, node.row, node.column, "Final abort message"))
        
        self.register_instruction(cil.PrintNode(final_msg, node.row, node.column, "Print abort info"))

        self.register_instruction(cil.AbortNode(node.row, node.column, "Object Abort Node"))
        return "0"
    
    @visitor.when(cil.ObjectTypeNameNode)
    def visit(self, node, scope=None):
        instance = self.params[0]
        result = self.define_internal_local(row=node.row, column=node.column, comment=node.comment)
        self.register_instruction(cil.TypeOfNode(instance.name, result, node.row, node.column, "Object Type Name Node"))
        self.register_instruction(cil.TypeNameNode(result, result, node.row, node.column, "Object Type Name Node"))
        return result
    
    @visitor.when(cil.IntAbortNode)
    def visit(self, node:cil.IntAbortNode, scope=None):
        type_name = self.define_internal_local(node.row, node.column, "Type name address")
        abort_first_msg = self.define_internal_local(node.row, node.column, "First part of the abort message")
        final_msg = self.define_internal_local(node.row, node.column, "Final abort message")

        self.register_instruction(cil.LoadNode(type_name, self.int_name_data.name, node.row, node.column))
        self.register_instruction(cil.LoadNode(abort_first_msg, self.abort_data.name, node.row, node.column))
        self.register_instruction(cil.ConcatNode(final_msg, abort_first_msg, type_name, node.row, node.column, "Final abort message"))
        
        self.register_instruction(cil.PrintNode(final_msg, node.row, node.column, "Print abort info"))

        self.register_instruction(cil.AbortNode(node.row, node.column, "Object Abort Node Int"))
        return "0"
    
    @visitor.when(cil.IntTypeNameNode)
    def visit(self, node:cil.IntTypeNameNode, scope=None):
        type_name = self.define_internal_local(node.row, node.column, "Type name address")
        self.register_instruction(cil.LoadNode(type_name, self.int_name_data.name, node.row, node.column))
        return type_name
    
    @visitor.when(cil.BoolAbortNode)
    def visit(self, node:cil.BoolAbortNode, scope=None):
        type_name = self.define_internal_local(node.row, node.column, "Type name address")
        abort_first_msg = self.define_internal_local(node.row, node.column, "First part of the abort message")
        final_msg = self.define_internal_local(node.row, node.column, "Final abort message")

        self.register_instruction(cil.LoadNode(type_name, self.bool_name_data.name, node.row, node.column))
        self.register_instruction(cil.LoadNode(abort_first_msg, self.abort_data.name, node.row, node.column))
        self.register_instruction(cil.ConcatNode(final_msg, abort_first_msg, type_name, node.row, node.column, "Final abort message"))
        
        self.register_instruction(cil.PrintNode(final_msg, node.row, node.column, "Print abort info"))

        self.register_instruction(cil.AbortNode(node.row, node.column, "Object Abort Node Bool"))
        return "0"
    
    @visitor.when(cil.BoolTypeNameNode)
    def visit(self, node:cil.BoolTypeNameNode, scope=None):
        type_name = self.define_internal_local(node.row, node.column, "Type name address")
        self.register_instruction(cil.LoadNode(type_name, self.bool_name_data.name, node.row, node.column))
        return type_name

    @visitor.when(cil.StringConcatNode)
    def visit(self, node, scope=None):
        string1 = self.params[0]
        string2 = self.params[1]
        result = self.define_internal_local( node.row, node.column, "String Concat Node")
        self.register_instruction(cil.ConcatNode(result, string1.name, string2.name, node.row, node.column, "String Concat Node"))
        return result
    
    @visitor.when(cil.StringLengthNode)
    def visit(self, node, scope=None):
        string = self.params[0]
        result = self.define_internal_local( node.row, node.column, "String Length Node")
        self.register_instruction(cil.LengthNode(result, string.name, node.row, node.column, "String Length Node"))
        return result
        
    @visitor.when(cil.StringSubstringNode)
    def visit(self, node, scope=None):
        string = self.params[0]
        index = self.params[1]
        length = self.params[2]
        result = self.define_internal_local( node.row, node.column, "String Substring Node")
        self.register_instruction(cil.SubstringNode(result, string.name, index.name, length.name, node.row, node.column,"String Substring Node"))
        return result
    
    @visitor.when(cil.IOInStringNode)
    def visit(self, node, scope=None):
        result = self.define_internal_local( node.row, node.column, "IO In String Node")
        self.register_instruction(cil.ReadNode(result, node.row, node.column, "IO In String Node"))
        return result

    @visitor.when(cil.IOInIntNode)
    def visit(self, node, scope=None):
        result = self.define_internal_local( node.row, node.column, "IO In Int Node")
        self.register_instruction(cil.ReadIntNode(result, node.row, node.column, "IO In Int Node"))
        return result
    
    @visitor.when(cil.IOOutIntNode)
    def visit(self, node, scope=None):
        integer = self.params[1]
        self.register_instruction(cil.PrintIntNode(integer.name, node.row, node.column, "IO Out Int Node"))
        return self.params[0].name
    
    @visitor.when(cil.IOOutStringNode)
    def visit(self, node, scope=None):
        string = self.params[1]
        self.register_instruction(cil.PrintNode(string.name, node.row, node.column, "IO Out String Node"))
        return self.params[0].name

    # ======================================================================
