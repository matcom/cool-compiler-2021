from Semantic.scope import VariableInfo
from Semantic import visitor
import itertools as itt


class Node:
    pass

class ProgramNode(Node):
    """
    nodo raiz
    """
    def __init__(self, dottypes, dotdata, dotcode):
        self.dottypes = dottypes
        self.dotdata = dotdata
        self.dotcode = dotcode

class TypeNode(Node):
    """
    Tipos definidos en el programa cool
    """
    def __init__(self, name, parent):
        self.name = name
        self.parent = parent
        self.attributes = []
        self.methods = []

class DataNode(Node):
    """
    Variables definidas en el programa
    """
    def __init__(self, vname, value):
        self.name = vname
        self.value = value

class FunctionNode(Node):
    """
    Funciones declaradas en el programa
    """
    def __init__(self, fname, params, localvars, instructions):
        self.name = fname
        self.params = params
        self.localvars = localvars
        self.instructions = instructions

class ParamNode(Node):
    def __init__(self, name):
        self.name = name

class LocalNode(Node):
    def __init__(self, name):
        self.name = name

class InstructionNode(Node):
    pass

class AssignNode(InstructionNode):
    """
    Asignacion del valor de `source` a la variable `dest`
    """
    def __init__(self, dest, source):
        self.dest = dest
        self.source = source

class UnaryOperationNode(InstructionNode):
    def __init__(self, dest, source):
        self.dest = dest
        self.source = source

class IntComplementNode(UnaryOperationNode):
    """
    Asignacion del valor de `~ source` a la variable `dest`
    """
    pass

class BoolComplementNode(UnaryOperationNode):
    """
    Asignacion del valor de `not source` a la variable `dest`
    """
    pass

class BinaryOperationNode(InstructionNode):
    def __init__(self, dest, left, right):
        self.dest = dest
        self.left = left
        self.right = right

class PlusNode(BinaryOperationNode):
    """
    Asignacion del valor de `left + right` a la variable `dest`
    """
    pass

class MinusNode(BinaryOperationNode):
    """
    Asignacion del valor de `left - right` a la variable `dest`
    """
    pass

class StarNode(BinaryOperationNode):
    """
    Asignacion del valor de `left * right` a la variable `dest`
    """
    pass

class DivNode(BinaryOperationNode):
    """
    Asignacion del valor de `left / right` a la variable `dest`
    """
    pass

class GetAttribNode(InstructionNode):
    """
    Asignacion del valor del `numb+1`-iesimo atributo de la instancia `_instance` a la variable `dest`
    """
    def __init__(self, dest, _instance, numb):
        self.dest = dest
        self.instance = _instance
        self.pos = numb

class SetAttribNode(InstructionNode):
    """
    Asignacion del valor de la variable `source` al `numb+1`-esimo atributo de la instancia `_instance`
    """
    def __init__(self, _instance, numb, source):
        self.source = source
        self.instance = _instance
        self.pos = numb

class AllocateNode(InstructionNode):
    """
    Liberar espacio en memoria para crear un objeto de tipo `itype` y almacenar su direccion
    en la variable `dest` (si es de tipo Int, Bool o String, se inicializa con el valor `value`)
    """
    def __init__(self, itype, dest, value = None):
        self.type = itype
        self.dest = dest
        self.value = value

class TypeOfNode(InstructionNode):
    """
    Obtiene el tipo del objeto `obj` y almacena la direccion del tipo en `dest`
    """
    def __init__(self, obj, dest):
        self.obj = obj
        self.dest = dest

class LabelNode(InstructionNode):
    """
    Crea un label de nombre `name`
    """
    def __init__(self, name):
        self.name = name

class GotoNode(InstructionNode):
    """
    Salta a la direccion donde se encuentra el label `label.name`
    """
    def __init__(self, label):
        self.label = label

class GotoIfNode(InstructionNode):
    """
    Si `vname` evalua True, salta a la direccion donde se encuentra el label `goto_label`
    """
    def __init__(self, vname, goto_label):
        self.vname = vname
        self.goto_label = goto_label

class StaticCallNode(InstructionNode):
    """
    Realiza un llamado a la funcion `function` y almacena el valor de retorno en `dest`
    """
    def __init__(self, function, dest):
        self.function = function
        self.dest = dest

class DynamicCallNode(InstructionNode):
    """
    Realiza un llamado a la funcion `function` de la clase `xtype` y almacena el valor de retorno en `dest`
    """
    def __init__(self, xtype, function, dest):
        self.xtype = xtype
        self.function = function
        self.dest = dest

class ArgNode(InstructionNode):
    """
    Carga el valor de la variable `name` antes del llamado a una funcion
    """
    def __init__(self, name):
        self.name = name

class ReturnNode(InstructionNode):
    """
    Retorna el valor de `ret`
    """
    def __init__(self, ret = None):
        self.ret = ret

class RunTimeNode(InstructionNode):
    """
    Retorna el valor de `ret`
    """
    def __init__(self, error):
        self.error = error

class EndProgramNode(InstructionNode):
    pass

class CopyNode(InstructionNode):
    """
    Copia el valor de `obj` y lo almacena en la variable `dest`
    """
    def __init__(self, dest, obj):
        self.dest = dest
        self.obj = obj

class LoadNode(InstructionNode):
    """
    Carga la direccion de `msg` en la variable `dest`
    """
    def __init__(self, dest, msg):
        self.dest = dest
        self.msg = msg

class BranchEqualNode(InstructionNode):
    """
    Realiza un salto hacia el label `label` si los valores de las variables `left` y `right`
    son iguales
    """
    def __init__(self, left, right, label):
        self.left = left
        self.right = right
        self.label = label

class BranchLTNode(InstructionNode):
    """
    Realiza un salto hacia el label `label` si el valor de la variable `left` es menor que
    el valor de la variable `right`
    """
    def __init__(self, left, right, label):
        self.left = left
        self.right = right
        self.label = label
        
class BranchLENode(InstructionNode):
    """
    Realiza un salto hacia el label `label` si el valor de la variable `left` es menor o igual que
    el valor de la variable `right`
    """
    def __init__(self, left, right, label):
        self.left = left
        self.right = right
        self.label = label

class Scope:
    def __init__(self, parent=None):
        self.locals = []
        self.parent = parent
        self.children = []
        self.local_by_name = dict()
        self.index = 0 if parent is None else len(parent)

    def __len__(self):
        return len(self.locals)

    def create_child(self):
        child = Scope(self)
        self.children.append(child)
        child.parent = self
        return child

    def define_variable(self, name, cil_name, vtype):
        info = VariableInfo(cil_name, vtype)
        self.locals.append(info)
        self.local_by_name[name] = info
        return info

    def find_variable(self, vname, index = None):
        locals = self.locals if index is None else itt.islice(self.locals, index)
        try:
            return next(x for x in locals if x.name == vname)
        except StopIteration:
            return self.parent.find_variable(vname, self.index) if self.parent is None else None

    def is_defined(self, vname):
        return self.find_variable(vname) is not None

    def is_local(self, vname):
        return any(True for x in self.locals if x.name == vname)