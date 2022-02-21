from typing import Dict, List


class Node:
    pass

class CILProgram:NotImplemented

class CILDeclaration(Node):
    pass


#function entry {
#    LOCAL lmsg ;
#    LOCAL instance ;
#    LOCAL result ;
#
#    lmsg = LOAD s1 ;
#    instance = ALLOCATE Main ;
#    SETATTR instance Main_msg lmsg ;
#
#    ARG instance ;
#    result = VCALL Main Main_main ;
#
#    RETURN 0 ;
#}
class CILFuncDeclaration(CILDeclaration):
    def __init__(self, id:str):
        self.id:str = id
        self.params:List(str) = []
        self.locals:List(str)=[]
        self.instructions:List(CILInstruction) = []
    
    def add_params(self,params:List(str),pos=None):
        if pos:
            for x in reversed(params):
                self.params.insert(pos,x)
        else:        
            for x in params:self.params.append(x)

    def add_locals(self,locals:List(str),pos=None):
        if pos:
            for x in reversed(locals):
                self.locals.insert(pos,x)
        else:        
            for x in locals:self.locals.append(x)

    def add_instruction(self,instructions:List(str),pos=None):
        if pos:
            for x in reversed(instructions):
                self.instructions.insert(pos,x)
        else:        
            for x in instructions:self.instructions.append(x)



class CILInstruction(Node):
    pass

### Asignación simple
#x = y ;
class CILSimpleAssignInstruction(CILInstruction):
    def __init__(self, id,expr):
        self.id = id
        self.expr=expr
    def __str__(self):
        return f"{self.id} = {self.expr}"


class CILBinaryInstruction(CILInstruction):
    def __init__(self,id,left,right):
        super().__init__()
        self.id=id
        self.left=left
        self.right=right

### Operaciones aritméticas
class CILArithBinaryInstruction(CILBinaryInstruction):pass

#x = y + z ;
class CILPlusInstruction(CILArithBinaryInstruction):
    def __init__(self, id, left, right):
        super().__init__(id, left, right)
    def __str__(self):
        return f"{self.id} = {self.left} + {self.right}"

#x = y - z ;
class CILMinusInstruction(CILArithBinaryInstruction):
    def __init__(self, id, left, right):
        super().__init__(id, left, right)
    def __str__(self):
        return f"{self.id} = {self.left} - {self.right}"

#x = y * z ;
class CILStarInstruction(CILArithBinaryInstruction):
    def __init__(self, id, left, right):
        super().__init__(id, left, right)
    def __str__(self):
        return f"{self.id} = {self.left} * {self.right}"

#x = y / z ;
class CILDivInstruction(CILArithBinaryInstruction):
    def __init__(self, id, left, right):
        super().__init__(id, left, right)
    def __str__(self):
        return f"{self.id} = {self.left} / {self.right}"

class CILBooleanBinaryInstruction(CILBinaryInstruction):pass

class CILLessInstruction(CILBooleanBinaryInstruction):
    def __init__(self, id, left, right):
        super().__init__(id, left, right)
    def __str__(self):
        return f"{self.id} = {self.left} < {self.right}"    

class CILLessEqualInstruction(CILBooleanBinaryInstruction):
    def __init__(self, id, left, right):
        super().__init__(id, left, right)
    def __str__(self):
        return f"{self.id} = {self.left} <= {self.right}"    

class CILEqualInstruction(CILBooleanBinaryInstruction):
    def __init__(self, id, left, right):
        super().__init__(id, left, right)
    def __str__(self):
        return f"{self.id} = {self.left} == {self.right}"    

class CILNoEqualInstruction(CILBooleanBinaryInstruction):
    def __init__(self, id, left, right):
        super().__init__(id, left, right)
    def __str__(self):
        return f"{self.id} = {self.left} != {self.right}"    

### Acceso a atributos

#x = GETATTR y b ;
#Es equivalente a `x = y.b`.
class CILGETATTRInst(CILInstruction):
    def __init__(self, id,y,attr):
        self.id = id
        self.y=y
        self.attr=attr
    def __str__(self):
        return f"{self.id} = GETATTR {self.y} {self.attr}"

#SETATTR y b x ;
#Es equivalente a `y.b = x`.
class CILSETATTRInst(CILInstruction):
    def __init__(self,y,attr,value):
        self.y=y
        self.attr=attr
        self.value = value
    def __str__(self):
        return f"SETATTR {self.y} {self.attr} {self.value}"

### Acceso a arrays

#Acceder al iésimo elemento:
#x = GETINDEX a i ;
class CILGETINDEXInst(CILInstruction):
    def __init__(self,id,array,index):
        self.id=id
        self.array=array
        self.index=index
    def __str__(self):
        return f"{self.id} = GETINDEX {self.array} {self.index}"

#Asignar un valor
#SETINDEX a i x ;
class CILSETINDEXInst(CILInstruction):
    def __init__(self,array,index,value):
        self.array=array
        self.index=index
        self.value=value
    def __str__(self):
        return f"SETINDEX {self.array} {self.index} {self.value}"

### Manipulación de memoria


#Instrucción de alocación de memoria:
#x = ALLOCATE T ;
#Esta instrucción crea en memoria espacio suficiente para alojar un tipo `T`
#devuelve en `x` la dirección de memoria de inicio del tipo.
class CILALLOCATEInst(CILInstruction):
    def __init__(self,id,type):
        self.id=id
        self.type=type
    def __str__(self):
        return f"{self.id} = ALLOCATE {self.type}"

#Obtener el tipo dinámico de una variable
#t = TYPEOF x ;
class CILTYPEOFInst(CILInstruction):
    def __init__(self,type,var):
        self.type=type
        self.var=var
    def __str__(self):
        return f"{self.type} = TYPEOF {self.var}"

#Para crear arrays se utiliza una sintaxis similar
#x = ARRAY y ;
#Donde `y` es una variable de tipo numérico (como todas) que define el tamaño del array.
class CILARRAYInst(CILInstruction):
    def __init__(self,id,size):
        self.id=id
        self.size=size
    def __str__(self):
        return f"{self.id} = ARRAY {self.size}"

### Invocación de métodos
#Para invocar un método se debe indicar el tipo donde se encuentra el método,
#además del método en concreto que se desea ejecutar.
#Este llamado es una invocación estática, es decir, se llama exactamente al método `f`.
#x = CALL f ;
class CILCALLInst(CILInstruction):
    def __init__(self,id,meth):
        self.id=id
        self.meth=meth
    def __str__(self):
        return f"{self.id} = CALL {self.meth}"


#Llamado dinámico, donde el método `f` se buscan en el tipo `T` y se resuelve 
#la dirección del método real al que invocar:
#x = VCALL T f ;
class CILVCALLInst(CILInstruction):
    def __init__(self,id,meth,type):
        self.id=id
        self.meth=meth
        self.type=type
    def __str__(self):
        return f"{self.id} = VCALL {self.type} {self.meth}"

#Todos los parámetros deben ser pasados de antemano, con la siguiente instrucción:
#ARG a ;
class CILARGInst(CILInstruction):
    def __init__(self,params):
        self.params=params
    def __str__(self):
        return f"ARG {self.params}"

### Saltos
#Donde `label` tiene que ser una etiqueta declarada en algún lugar de la propia función.
# La etiqueta puede estar declarada después de su uso. 
#LABEL label ;
class CILLABELInst(CILInstruction):
    def __init__(self,id):
        self.id=id
    def __str__(self):
        return f"LABEL {self.id}"

#Los saltos incondicionales simplemente se ejecutan con:
#GOTO label ;
class CILGOTOInst(CILInstruction):
    def __init__(self,label):
        self.label=label
    def __str__(self):
        return f"GOTO {self.label}"

#IF x GOTO label ;
class CILIFGOTOInst(CILInstruction):
    def __init__(self,condition,label):
        self.condition=condition
        self.label=label
    def __str__(self):
        return f"IF {self.condition} GOTO {self.label}"

### Retorno de Función
#Esta instrucción pone el valor de `x` en la dirección de retorno de `f` y
#termina la ejecución de la función.
#RETURN x ;
#RETURN ;
class CILRETURNInst(CILInstruction):
    def __init__(self,value=None):
        self.value=value
    def __str__(self):
        if self.value is None:
            return f"RETURN "
        return f"RETURN {self.value}"    


### Funciones de cadena

#Las cadenas de texto se pueden manipular con funciones especiales.
#x = LOAD msg ;
class CILLOADInst(CILInstruction):
    def __init__(self,id,msg):
        self.id=id
        self.msg=msg
    def __str__(self):
        return f"{self.id} = LOAD {self.msg}"    

#y = LENGTH x ;
class CILLENGTHInst(CILInstruction):
    def __init__(self,id,chain):
        self.id=id
        self.chain=chain
    def __str__(self):
        return f"{self.id} = LENGTH {self.chain}"    

#y = CONCAT x z ;
class CILCONCATInst(CILInstruction):
    def __init__(self, id, chain1, chain2):
        self.id=id
        self.chain1=chain1
        self.chain2=chain2

    def __str__(self):
        return f"{self.id} = CONCAT {self.chain1} {self.chain2}"    

#y = SUBSTRING chain chain ;
class CILSUBSTRINGInst(CILInstruction):
    def __init__(self, id, chain1, chain2):
        self.id=id
        self.chain1=chain1
        self.chain2=chain2

    def __str__(self):
        return f"{self.id} = SUBSTRING {self.chain1} {self.chain2}"    

#Computa la representación textual de un valor numérico y devuelve la dirección en memoria:
#z = STR y ;
class CILSTRInst(CILInstruction):
    def __init__(self,id,chain):
        self.id=id
        self.chain=chain
    def __str__(self):
        return f"{self.id} = STR {self.chain}"    

### Operaciones IO

#READ lee de la entrada estándar hasta el siguiente cambio de línea (incluído)
#x = READ ;
class CILREADIntInst(CILInstruction):
    def __init__(self,id:str):
        self.id:str=id
    def __str__(self):
        return f"{self.id} = READ"    

class CILREADStringInst(CILInstruction):
    def __init__(self,id:str):
        self.id:str=id
    def __str__(self):
        return f"{self.id} = READ"    

#PRINT imprime en la salida estándar, sin incluir el cambio de línea
#PRINT z ;
class CILPRINTInst(CILInstruction):
    def __init__(self,id:str):
        self.id:str=id
    def __str__(self):
        return f"PRINT {self.id}"    

class CILVoidInstruction(CILInstruction):
    def __init__(self,expr):
        self.expr=expr

    def __str__(self):
        return f"Is Void? {self.expr}"
