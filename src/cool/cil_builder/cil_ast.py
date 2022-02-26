import cool.cmp.visitor as visitor


class CilNode:
    pass

class ProgramCilNode(CilNode):
    def __init__(self, dottypes, dotdata, dotcode):
        self.dottypes = dottypes
        self.dotdata = dotdata
        self.dotcode = dotcode

class TypeCilNode(CilNode):
    def __init__(self, name):
        self.name = name
        self.attributes = []
        self.methods = []

class DataCilNode(CilNode):
    def __init__(self, vname, value):
        self.name = vname
        self.value = value

class FunctionCilNode(CilNode):
    def __init__(self, fname, params, localvars, instructions):
        self.name = fname
        self.params = params
        self.localvars = localvars
        self.instructions = instructions

class ParamCilNode(CilNode):
    def __init__(self, name):
        self.name = name

class LocalCilNode(CilNode):
    def __init__(self, name):
        self.name = name

class InstructionCilNode(CilNode):
    pass


class BinaryCilNode(InstructionCilNode): #Binary Operations
    def __init__(self, dest, left, right):
        self.dest = dest
        self.left = left
        self.right = right

class UnaryCilNode(InstructionCilNode): #Unary Operations
    def __init__(self, dest, right):
        self.dest = dest
        self.right = right



class ConstantCilNode(InstructionCilNode): #7.1 Constant
    def __init__(self,vname,value):
        self.vname = vname
        self.value = value

#7.2 Identifiers, not necesary cil Node

class AssignCilNode(InstructionCilNode): # 7.3 Assignment
    def __init__(self, dest, source):
        self.dest = dest
        self.source = source

class StaticCallCilNode(InstructionCilNode): #7.4 Distaptch Static id.()
    def __init__(self,type,method_name,args, result):
        # self.expresion_instance = expresion_instance
        self.type = type
        self.method_name = method_name
        self.args = args
        self.result = result

class DynamicCallCilNode(InstructionCilNode): #7.4 Dispatch Dynamic <expr>.id()
    def __init__(self, expresion_instance,static_type, method_name,args, result):
        self.expresion_instance = expresion_instance
        self.static_type = static_type
        self.method_name = method_name
        self.args = args
        self.result = result

class DynamicParentCallCilNode(InstructionCilNode): #7.4 Dispatch <expr>@type.id()
    def __init__(self, expresion_instance,static_type, method_name,args, result):
        self.expresion_instance = expresion_instance
        self.static_type = static_type
        self.method_name = method_name
        self.args = args
        self.result = result


# class IfCilNode(InstructionCilNode): #7.5 If Conditional
#     def __init__(self,if_expr,then_label,else_label):
#         self.if_expr = if_expr
#         self.then_label = then_label
#         self.else_label = else_label

# class WhileCilNode(InstructionCilNode): #7.6 Loops
#     def __init__(self,condition,body):
#         self.condition = condition
#         self.body = body

class BlockCilNode(InstructionCilNode): #7.7 Blocks
    pass

class LetCilNode(InstructionCilNode): #7.8 Let
    pass

class CaseCilNode(InstructionCilNode): #7.9 Case
    def __init__(self,expr):
        self.main_expr = expr

class BranchCilNode(InstructionCilNode): #7.9 Case
    def __init__(self,type_k):
        self.type_k = type_k

class CaseEndCilNode(InstructionCilNode): #7.9 Case
    def __init__(self,result):
        self.result = result


class InstantiateCilNode(InstructionCilNode): #7.10 New
    pass

class IsVoidCilNode(InstructionCilNode): #7.11 IsVoid
    def __init__(self, expresion, result):
        self.expresion = expresion
        self.result = result
    pass


#Binary Aritmetic Operations
class PlusCilNode(BinaryCilNode): 
    pass

class MinusCilNode(BinaryCilNode):
    pass

class StarCilNode(BinaryCilNode):
    pass
class DivCilNode(BinaryCilNode):
    pass

class EqualCilNode(BinaryCilNode):
    pass

class CompareStringCilNode(BinaryCilNode):
    pass

class EqualRefCilNode(BinaryCilNode):
    pass
class LessEqualCilNode(BinaryCilNode):
    pass

class LessCilNode(BinaryCilNode):
    pass
class IsVoidCilNode(UnaryCilNode):
    pass
class NotCilNode(UnaryCilNode):
    pass
class NegateCilNode(UnaryCilNode):
    pass




# Attributes operations
class GetAttribCilNode(InstructionCilNode):
    #instance es la direccion de memoria donde se encuentra la instancia en memoria
    #Type es el tipo estatico de esa instancia 
    #attribute es el atributo de ese tipo al que se quiere acceder
    #result es la direccion de memoria (el local internal) donde voy a guardar el valor del atributo
    #Con el tipo estatico + el atributo puedo saber el offset
    def __init__(self,instance,type,attribute,result):
        self.instance = instance
        self.type = type
        self.attribute = attribute
        self.result = result

class SetAttribCilNode(InstructionCilNode):
    #instance es la direccion de memoria donde se encuentra la instancia en memoria
    #Type es el tipo estatico de esa instancia 
    #attribute es el atributo de ese tipo al que se quiere guardar la informacion
    #value es la direccion de memoria (el local internal) donde se encuentra el valor que deseo guardar en el atributo
    #Con el tipo estatico + el atributo puedo saber el offset
    def __init__(self,instance,type,attribute,value):
        self.instance = instance
        self.type = type
        self.attribute = attribute
        self.value = value

class SetDefaultCilNode(InstructionCilNode):
    def __init__(self,instance,type,attribute,value):
        self.instance = instance
        self.type = type
        self.attribute = attribute
        self.value = value

class AllocateCilNode(InstructionCilNode):
    #Liberar espacio en el heap para la instancia y la direccion de memoria donde se creo dejarla en result
    #result seria una local internal con la direccion en memoria de la instancia creada
    def __init__(self, type, result):
        self.type = type
        self.result = result

class AllocateDynamicCilNode(InstructionCilNode):
    #Liberar espacio en memoria a partir de una cantidad que se encuentra en una direccion de memoria.
    def __init__(self,address_in_local,result):
        self.address_in_local = address_in_local
        self.result = result

class InternalCopyCilNode(InstructionCilNode):
    def __init__(self,dir_child,dir_ancestor):
        self.dir_child = dir_child
        self.dir_ancestor = dir_ancestor

class GetDataCilNode(InstructionCilNode):
    def __init__(self,name,result):
        self.name = name
        self.result = result

class TypeOfCilNode(InstructionCilNode):
    #Dado una instancia (local internal que posee una direccion en memoria con el tipo dinamico) devolver el string correspondiente a ese tipo dinamico
    def __init__(self, instance, result):
        self.instance = instance
        self.result = result

class LabelCilNode(InstructionCilNode):
    def __init__(self,label):
        self.label = label

class GotoCilNode(InstructionCilNode):
    def __init__(self,label):
        self.label = label

class GotoIfCilNode(InstructionCilNode):
    def __init__(self,val_dir,label):
        self.val_dir = val_dir
        self.label = label

class GotoBoolIfCilNode(InstructionCilNode):
    def __init__(self,val_dir,label):
        self.val_dir = val_dir
        self.label = label
class NotGotoIfCilNode:
    def __init__(self,val_dir,label):
        self.val_dir = val_dir
        self.label = label

class ArgCilNode(InstructionCilNode):
    #En result se guardaria la direccion en memoria donde esta el resultado de evaluar la expresion del argumento
    def __init__(self, result):
        self.result = result

class ReturnCilNode(InstructionCilNode):
    #Direccion en memoria donde se guarda el resultado de la funcion
    def __init__(self, value=None):
        self.value = value


#TypesCilNodes
class IntCilNode(InstructionCilNode):
    def __init__(self,value,result):
        self.value = value
        self.result = result

class StringCilNode(InstructionCilNode):
    def __init__(self,dir1,dir2):
        self.dir1 = dir1
        self.dir2 = dir2

#Function CilNodes
class ToStrCilNode(InstructionCilNode):
    def __init__(self, dest, ivalue):
        self.dest = dest
        self.ivalue = ivalue

class ReadCilNode(InstructionCilNode):
    def __init__(self,dest):
        self.dest = dest

class PrintCilNode(InstructionCilNode):
    def __init__(self,to_print):
        self.to_print = to_print
class AbortCilNode(InstructionCilNode):
    def __init__(self,self_from_call):
        self.self_from_call = self_from_call
class TypeNameCilNode(InstructionCilNode):
    def __init__(self, self_param, result):
        self.self_param = self_param
        self.result = result
class CopyCilNode(InstructionCilNode):
    def __init__(self, self_param, result):
        self.self_param = self_param
        self.result = result
class PrintStringCilNode(PrintCilNode):
    pass
class PrintIntCilNode(PrintCilNode):
    pass
class ReadStringCilNode(ReadCilNode):
    pass
class ReadStrEndCilNode(InstructionCilNode):
    def __init__(self, length,result):
        self.length = length
        self.result = result
class ReadIntCilNode(ReadCilNode):
    pass
class LengthCilNode(InstructionCilNode):
    def __init__(self, self_dir, length):
        self.self_dir = self_dir
        self.length = length
class ConcatCilNode(InstructionCilNode):
    def __init__(self, self_param, param_1,result_addr):
        self.self_param = self_param
        self.param_1 = param_1
        self.result_addr = result_addr

class SubstringCilNode(InstructionCilNode):
    def __init__(self, self_param,value1, value2,result):
        self.self_param = self_param
        self.value1 = value1
        self.value2 = value2
        self.result = result


#Given 2 memory location calculate the distance of his types
class TypeDistanceCilNode(InstructionCilNode):
    def __init__(self,type1,type2,result):
        self.type1 = type1
        self.type2 = type2
        self.result = result 


class MinCilNode(InstructionCilNode):
    def __init__(self,num1,num2,result):
        self.num1 = num1
        self.num2 = num2
        self.result = result



class ErrorCilNode(InstructionCilNode):
    def __init__(self,name):
        self.name = name


############# New Nodes ###################     
def get_formatter():
    class PrintVisitor(object):
        @visitor.on('CilNode')
        def visit(self, CilNode):
            pass

        @visitor.when(ProgramCilNode)
        def visit(self, CilNode):
            dottypes = '\n'.join(self.visit(t) for t in CilNode.dottypes)
            dotdata = '\n'.join(self.visit(t) for t in CilNode.dotdata)
            dotcode = '\n'.join(self.visit(t) for t in CilNode.dotcode)

            return f'.TYPES\n{dottypes}\n\n.DATA\n{dotdata}\n\n.CODE\n{dotcode}'

        @visitor.when(TypeCilNode)
        def visit(self, CilNode):
            attributes = '\n\t'.join(f'attribute {x}' for x in CilNode.attributes)
            methods = '\n\t'.join(f'method {x}: {y}' for x,y in CilNode.methods)

            return f'type {CilNode.name} {{\n\t{attributes}\n\n\t{methods}\n}}'

        @visitor.when(FunctionCilNode)
        def visit(self, CilNode):
            params = '\n\t'.join(self.visit(x) for x in CilNode.params)
            localvars = '\n\t'.join(self.visit(x) for x in CilNode.localvars)
            instructions = '\n\t'.join(self.visit(x) for x in CilNode.instructions)

            return f'function {CilNode.name} {{\n\t{params}\n\n\t{localvars}\n\n\t{instructions}\n}}'

        @visitor.when(ParamCilNode)
        def visit(self, CilNode):
            return f'PARAM {CilNode.name}'

        @visitor.when(LocalCilNode)
        def visit(self, CilNode):
            return f'LOCAL {CilNode.name}'

        @visitor.when(AssignCilNode)
        def visit(self, CilNode):
            return f'{CilNode.dest} = {CilNode.source}'

        @visitor.when(PlusCilNode)
        def visit(self, CilNode):
            return f'{CilNode.dest} = {CilNode.left} + {CilNode.right}'

        @visitor.when(MinusCilNode)
        def visit(self, CilNode):
            return f'{CilNode.dest} = {CilNode.left} - {CilNode.right}'

        @visitor.when(StarCilNode)
        def visit(self, CilNode):
            return f'{CilNode.dest} = {CilNode.left} * {CilNode.right}'

        @visitor.when(DivCilNode)
        def visit(self, CilNode):
            return f'{CilNode.dest} = {CilNode.left} / {CilNode.right}'

        @visitor.when(AllocateCilNode)
        def visit(self, CilNode):
            return f'{CilNode.dest} = ALLOCATE {CilNode.type}'

        @visitor.when(TypeOfCilNode)
        def visit(self, CilNode):
            return f'{CilNode.dest} = TYPEOF {CilNode.type}'

        @visitor.when(StaticCallCilNode)
        def visit(self, CilNode):
            return f'{CilNode.dest} = CALL {CilNode.function}'

        @visitor.when(DynamicCallCilNode)
        def visit(self, CilNode):
            return f'{CilNode.dest} = VCALL {CilNode.type} {CilNode.method}'

        @visitor.when(ArgCilNode)
        def visit(self, CilNode):
            return f'ARG {CilNode.name}'

        @visitor.when(ReturnCilNode)
        def visit(self, CilNode):
            return f'RETURN {CilNode.value if CilNode.value is not None else ""}'

    printer = PrintVisitor()
    return (lambda ast: printer.visit(ast))