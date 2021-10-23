from cool_compiler.semantic.visitor import result
from .__dependency import CoolTypeBuildInManager, SemanticError, ErrorType, Type, Object 
from .v2_semantic_checking.scope import Scope

def defVisitClass(*func):
    class Visit(VisitBase):
        def visit(self, node,*args, **kw):
            error_handler = self.gclss.get_se_handler(node)
            result = []
            for f in func:
                result.append(f(self, node, error_handler,*args, **kw))
            return tuple(result)
    return Visit

class VisitBase:
    def get_type(self, type_name, error_handler):
        find_result = find_type(type_name, self.global_types)
        return find_result.get_value( if_fail_do= error_handler().add_semantic_error )
    
    def visit_all(self, list_node, *args):
        result = []
        for n in list_node:
            result.append(self.visit(n, *args))
        
        return result
    
    def get_se_handler(self, node):
        return self.cool_error.get_handler(node.lineno, node.index)


    def get_parent_type(self, node, error_handler):
        if node.parent is None: return Object()
            
        find_result = find_type(node.parent, self.global_types)
        parent_type = find_result.get_value( if_fail_do= error_handler().add_semantic_error )
            
        if parent_type.is_shield or parent_type.name == self.current_type.name: 
            error_handler().add_semantic_error( f"class {self.current_type.name} can't be inherited from {parent_type.name}" )
            return ErrorType()

        return parent_type 


class VisitorBase:
    def __init__(self, error) -> None:
        self.cool_error = error
        self.current_type : Type = None
    
    def type_checking(self, tbase : Type, ttype : Type):
        if tbase.is_self_type : tbase = self.current_type
        if ttype.is_self_type : ttype = self.current_type

        if not ttype.conforms_to(tbase):
            return False
        
        return True

class Result:
    def __init__(self, succ, result, error) -> None:
        self.succ = succ
        self.result = result
        self.error = error
    
    def get_value(self, if_fail_do = None):
        if self.succ:  return self.result

        if_fail_do(self.error)
        return self.result

    @staticmethod
    def ok(result):
        return Result(True, result, "")
    
    @staticmethod
    def fail(error, neutro = None):
        return Result(False, neutro, error)


def find_type(name, global_types) -> Result:
    if name in global_types:
        return Result.ok( global_types[name] )
    try:
        return Result.ok( CoolTypeBuildInManager().find(name) )
    except SemanticError as se:        
        return Result.fail( se.text, neutro = ErrorType() )

def parent_common(self, t1: Type, t2: Type):
    while True:
        if None in (t1,t2): return Object()
        if t1.conforms_to(t2): return t2
        if t2.conforms_to(t1): return t1

        t1 = t1.parent
        t2 = t2.parent

def find_variable(self, name, scope: Scope, node) -> Result:
    try: 
        v = scope.find_variable(name)
        return Result.ok (v.type)
    except SemanticError:
        self.cool_error(node.lineno, node.index).add_name_error(name)
        return Result.fail(name, neutro = ErrorType() )
