from Parser.ast import ProgramNode
from Tools import TypeException, visitor
from Tools import Token, Context, SemanticErrors

class TypeCollector:
    def __init__(self, errors):
        self.type_level = {}
        self.errors = errors

    @visitor.on('node')
    def visit(self, node):
        pass

    @visitor.when(ProgramNode)
    def visit(self, node):
        self.context = Context()
        
        for def_class in node.class_list:
            try:
                self.context.create_type(def_class.type.value)
                self.type_level[def_class.type.value] = def_class.parent
            except TypeException as error:
                self.errors.append(SemanticErrors(def_class.type.line, def_class.type.column, error))
        
        node.class_list.sort(key = lambda node: self.get_type_level(node.type))
        
        try:
            self.context.types['Main']
        except KeyError:
            self.errors.append(SemanticErrors(0,0, 'Class Main is not defined.'))
        
        return self.context
    
    def get_type_level(self, type):
            try:
                parent = self.type_level[type.value]
            except KeyError:
                return 0        
            if parent == 0:
                self.errors.append(SemanticErrors(type.line, type.column, f'Class {type.value}, or an ancestor of {type.value}, is involved in an inheritance cycle.'))
            elif not isinstance(parent, int):
                self.type_level[type.value] = 0 if parent else 1
                if isinstance(parent, Token):
                    self.type_level[type.value] = self.get_type_level(parent) + 1          
            return self.type_level[type.value] 