import cool_cmp.shared.visitor as visitor
from cool_cmp.shared.ast import BaseAST
from cool_cmp.semantic.interface import  IContext, ISemantic
from cool_cmp.shared.errors import ErrorTracker, IErrorTraceable, CoolError
from cool_cmp.shared.ast.cool import *
from cool_cmp.semantic.implementations import Context, CoolType
from cool_cmp.semantic.types import *
from cool_cmp.semantic.errors import SemanticError, TYPE_ALREADY_DEFINED, TYPE_NOT_DEFINED, \
    TYPE_CYCLIC_DEPENDENCY

class TypeCollectorVisitor(IErrorTraceable):
    """
    Collects the types by saving them to an IContext
    """
    
    def __init__(self):
        self.errors = ErrorTracker()
        self.context = Context()

    def add_semantic_error(self, error:SemanticError, line:int, pos:int):
        error.set_position(line, pos)
        self.add_error(error)
    
    @visitor.on('node')
    def visit(self, node):
        pass
    
    @visitor.when(ProgramNode)
    def visit(self, node:ProgramNode):
        
        if not self.context:
            obj = ObjectType()
            int_ = IntType(obj)
            bool_ = BoolType(obj)
            string = StringType(obj)
            io = IOType(obj)
            
            self.context = Context([
                obj,
                int_,
                bool_,
                string,
                io,
            ])
        
        default_names = [x.name for x in self.context.types]
        type_names = [x.name for x in default_names]
        
        for class_decl in node.declarations: # Collecting defined classes
            if class_decl.id in type_names:
                error = SemanticError(TYPE_ALREADY_DEFINED(class_decl.id))
                self.add_semantic_error(error, class_decl.row, class_decl.column)
            else:
                type_names.append(class_decl.id)
        
        for class_decl in node.declarations: # Verify that parent classes exist
            if class_decl.parent not in type_names:
                error = SemanticError(TYPE_NOT_DEFINED(class_decl.parent))
                self.add_semantic_error(error, class_decl.row, class_decl.column) # TODO row and column should point to 'parent' token position

        
        # Search for cyclic dependencies
        import cool_cmp.semantic.visitors.utils as ut
        graph = ut.build_graph_list([(x.id, x.parent) for x in node.declarations])
        cycles, sort = ut.any_cycles(graph)
        
        for cycle in cycles: # Adding cyclic dependency errors
            error = SemanticError(TYPE_CYCLIC_DEPENDENCY(cycle))
            self.add_error(error)
        
        for class_name in sort: # Defining types in topological order
            if class_name in default_names: # Class already in context
                continue
            
            class_decl = [x for x in node.declarations if x.id == class_name]
            if len(class_decl) != 1: # Error already captured. Multiple definitions or no definition
                continue
            
            class_decl = class_decl[0]
            
            # At this point shold work whitout the try except
            try:
                father = self.context.get_type(class_decl.parent)
            except SemanticError as exc:
                self.add_semantic_error(exc, class_decl.row, class_decl.column)

            try:
                self.context.add_type(class_decl, father)
            except SemanticError as exc:
                self.add_semantic_error(exc, class_decl.row, class_decl.column)
                
        return self.context
    
    def add_error(self, error:CoolError):
        self.errors.add_error(error)

    def get_errors(self)->List[CoolError]:
        self.errors.get_errors()

class CollectorService(ISemantic):
    
    
    def __init__(self):
        self._errors = ErrorTracker()
    
    @property
    def name(self)->str:
        return 'context'

    def __call__(self, ast:BaseAST) -> BaseAST:
        collector = TypeCollectorVisitor()
        context = collector.visit(ast.node)
        for error in collector.get_errors():
            self.add_error(error)
        return context
    
    def add_error(self, error:CoolError):
        self._errors.add_error(error)

    def get_errors(self)->List[CoolError]:
        return self._errors.get_errors()