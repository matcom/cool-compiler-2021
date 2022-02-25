errors_semantic = []

def append_error_semantic(fila, column, error):
    errors_semantic.append(f'({fila}, {column}) - {error}')


class Method:
    def __init__(self, id, parametros, returned_type):
        self.returnedType = returned_type
        self.id = id
        self.args = parametros

class Attribute:
    def __init__(self, id, atributoT, expression=None):
        self.id = id
        self.attrType = atributoT
        self.expression = expression


class Tipos:
    def __init__(self, nombre, tipo_padre, inherit=True):
        self.attributes = {}
        self.methods = {}
        self.childs = set()
        self.name = nombre
        self.order = 0
        self.min_order = 0
        self.parent = tipo_padre        
        self.inherit = inherit

    def __str__(self):
        return f'{self.name}'

    def __repr__(self):
        return f'{self.name}'

    def __repr__(self):
        return f'{self.id}{self.args}:{self.returnedType}'

    def my_attribute(self):
        return self.attributes.values()

    def my_method(self):
        return self.methods

    def add_method(self, id, typo_argumento, returned_type):
        type = self
        while type:
            try:
                method_type = type.methods[id]
                if len(method_type.args) != len(typo_argumento):
                    return False, f'SemanticError: invalid redefinition of {id}'
                for i in range(0, len(typo_argumento)):
                    type = TypesByName[typo_argumento[i]]
                    if type != method_type.args[i]:
                        return False, f'SemanticError: In redefined method {id}, parameter type {type} is different from original type {method_type.args[i]}.'
                respuesta = get_type(returned_type)
                if method_type.returnedType != respuesta:
                    return False, f'SemanticError: In redefined method {id}, return type {respuesta} is different from original return type {method_type.returnedType}.'
                break
            except KeyError:
                type = type.parent
        definido, error_msg = self.definelo(id)
        if definido:
            list_arg = []
            for arg in typo_argumento:
                arg_type = get_type(arg)
                if arg_type is None:
                    return False, f'TypeError: Class {arg} of formal parameter is undefined.'
                list_arg.append(arg_type)
            respuesta = get_type(returned_type)
            if respuesta is None:
                return False, f'TypeError: Undefined return type {returned_type} in method {id}.'
            self.methods[id] = Method(id, list_arg, respuesta)
            return True, None
        else:
            return False, error_msg

    def add_attr(self, id, atributoT, expression):
        attribute, _ = get_attribute(self, id)
        if attribute is not None:
            return False, f'SemanticError: Attribute {id} is an attribute of an inherited class.'
        try:
            x = self.attributes[id]
            return False, f'SemanticError: Attribute {id} is an attribute of an inherited class.'
        except KeyError:
            atributo = get_type(atributoT)
            if atributo is None:
                return False, f'TypeError: Class {atributoT} of attribute {id} is undefined.'
            self.attributes[id] = Attribute(id, atributo, expression)
            return True, None

    def get_method(self, id, parametros):
        try:
            return self.metodos_no_heredados(id, parametros)
        except Exception:
            if self.parent:
                return self.parent.get_method(id, parametros)
            else:
                return None, None, f'AttributeError: Dispatch to undefined method {id}.'

    def atributos(self):
        type = self
        result = []
        while type:
            atributo = []
            for attr in type.attributes.values():
                atributo.append(attr)
            result.append(atributo)
            type = type.parent
        return [elem for sublist in result[::-1] for elem in sublist]

    def definelo(self, id):
        if id in self.methods.keys():
            return False, f'SemanticError: Method {id} is multiply defined.'
        return True, None
   
    def metodos_heredados(self):
        type = self.parent
        result = []
        while type:
            metodo = []
            for method in type.methods.values():
                method.owner = type.name
                metodo.append(method)
            result.append(metodo)
            type = type.parent
        return [elem for sublist in result[::-1] for elem in sublist]
    

    def metodos_no_heredados(self, id, parametros):
        try:
            method = self.methods[id]
            if len(parametros) != len(method.args):
                return None, None, f'SemanticError: Method {id} called with wrong number of arguments.'
            for i, a in enumerate(parametros):
                if not check_herencia(a, method.args[i]):
                    return None, None, f'TypeError: In call of method {id}, type {a} does not conform to declared type {method.args[i]}.'
            return method, self, None
        except KeyError:
            raise Exception(f'type {self.name} don\'t have a method {id}')    

def join_set(a, b):
    h = jerarquia(b)
    while a is not None:
        if a in h:
            break
        a = a.parent
    return a

def get_type(type_name):
    try:
        return TypesByName[type_name]
    except KeyError:
        return None

def get_attribute(c: Tipos, id: str):
    while c is not None:
        try:
            return c.attributes[id], c
        except KeyError:
            c = c.parent
    return None, None   

def ordenado(type: Tipos, lugar: int) -> int:
    type.min_order = lugar
    for t in type.childs:
        lugar = ordenado(t, lugar)
    type.order = lugar
    return lugar + 1


def jerarquia(x):
    h = []
    while x is not None:
        h.append(x)
        x = x.parent
    return h

def check_herencia(a: Tipos, b: Tipos):
    index = a
    while index != b:
        if index is None:
            return False
        index = index.parent
    return True

def check_jerarquia(node):
    for c in node.classes:
        classT = TypesByName[c.type]
        if c.parent_type:
            try:
                padreT = TypesByName[c.parent_type]
                if padreT.inherit:
                    classT.parent = padreT
                    padreT.childs.add(classT)
                    x = padreT
                    while x:
                        if x == classT:
                            append_error_semantic(
                                c.lineno, c.colno, f'SemanticError: Class {classT.name}, or an ancestor of {classT.name}, is involved in an inheritance cycle.')
                            return False
                        x = x.parent
                else:
                    append_error_semantic(c.lineno, c.colno, f'SemanticError: Class {classT} cannot inherit class {padreT.name}.')
                    return False
            except KeyError:
                append_error_semantic(c.lineno, c.colno, f'TypeError: Class {classT} inherits from an undefined class {c.parent_type}.')
                return False
        else:
            classT.parent = ObjectType
            ObjectType.childs.add(classT)
    ordenado(ObjectType, 1)
    return True

def check_type(node):
    for c in node.classes:
        try:
            x = TypesByName[c.type]
            append_error_semantic(c.lineno, c.colno,
                               f'SemanticError: Redefinition of basic class {c.type}.')
            return False
        except KeyError:
            TypesByName[c.type] = Tipos(c.type, None)
    return True

SelfType = Tipos('SELF_TYPE', None, False)
ObjectType = Tipos('Object', None)
ObjectType.order = 0
IOType = Tipos('IO', ObjectType)
IOType.order = -1
IntType = Tipos('Int', ObjectType, False)
IntType.order = -2
StringType = Tipos('String', ObjectType, False)
StringType.order = -2
BoolType = Tipos('Bool', ObjectType, False)
BoolType.order = -2


TypesByName = {
    'SELF_TYPE': SelfType,
    'Object': ObjectType,
    'IO': IOType,
    'Int': IntType,
    'String': StringType,
    'Bool': BoolType
}

ObjectType.childs = set([IOType, IntType, StringType, BoolType])
ObjectType.add_method('abort', [], 'Object')
ObjectType.add_method('type_name', [], 'String')
ObjectType.add_method('copy', [], 'SELF_TYPE')
IOType.add_method('out_string', ['String'], 'SELF_TYPE')
IOType.add_method('out_int', ['Int'], 'SELF_TYPE')
IOType.add_method('in_string', [], 'String')
IOType.add_method('in_int', [], 'Int')
StringType.add_method('length', [], 'Int')
StringType.add_method('concat', ['String'], 'String')
StringType.add_method('substr', ['Int', 'Int'], 'String')

IntType.add_method('abort', [], 'Object')
BoolType.add_method('abort', [], 'Object')
StringType.add_method('abort', [], 'Object')

StringType.add_method('type_name', [], 'String')
IntType.add_method('type_name', [], 'String')
BoolType.add_method('type_name', [], 'String')

