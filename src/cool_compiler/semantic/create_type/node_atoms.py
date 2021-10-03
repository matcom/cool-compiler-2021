from .node__ import Expresion
from ..tools import defVisitClass
from ..factory_return_ast import Void as AST_Void
from ..factory_return_ast import New as AST_New
from ..factory_return_ast import Complement as AST_Complement
from ..factory_return_ast import Neg as AST_Neg
from ..factory_return_ast import Id as AST_Id
from ..factory_return_ast import Int as AST_Int
from ..factory_return_ast import Str as AST_Str
from ..factory_return_ast import Bool as AST_Bool

class Atomic(Expresion):
    def __init__(self, item) -> None:
        self.item = item
    
class Void(Atomic):
    pass
    
class New(Atomic):
    pass
    
class Complement(Atomic):
    pass
    
class Neg(Atomic):
    pass
    
class Id(Atomic):
    pass
    
class Int(Atomic):
    pass
    
class Str(Atomic):
    pass

class Bool(Atomic):
    pass

VisitAtomic = defVisitClass(
    lambda self, node, error: self.gclss.visit(node.item),
)

VisitNew = defVisitClass(
    lambda self, node, error: self.get_type(node.item, error),
)

VisitEqualAtomic = defVisitClass(
    lambda self, node, error: node.item,
)


 
