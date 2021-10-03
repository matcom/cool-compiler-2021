from .. import visitor
from ..__dependency import Type
from ..tools import  VisitorBase,
from .node_program import Program, VisitProgram, AST_Program
from .node_class import CoolClass, VisitCoolClass, AST_CoolClass
from .node_defattr import AtrDef, VisitAttrDef, AST_AtrDef
from .node_deffunc import  FuncDef, VisitFuncDef, AST_FuncDef

from .node_dispatch import CastingDispatch, VisitCastingDispatch, AST_CastingDispatch
from .node_dispatch import Dispatch, VisitDispatch, AST_Dispatch
from .node_dispatch import StaticDispatch, VisitStaticDispatch, AST_StaticDispatch

from .node_statements import Assing, VisitAssing, AST_Assing
from .node_statements import IfThenElse, VisitIfThenElse, AST_IfThenElse
from .node_statements import While, VisitWhile, AST_While
from .node_statements import Block, VisitBlock, AST_Block
from .node_let import LetIn, VisitLetIn, AST_LetIn
from .node_case import Case, VisitCase, AST_Case

from .node_binary import Sum, AST_Sum, VisitBinary
from .node_binary import Rest, AST_Rest
from .node_binary import Div, AST_Div
from .node_binary import Mult, AST_Mult
from .node_binary import Less, AST_Less
from .node_binary import LessOrEquals, AST_LessOrEquals
from .node_binary import Equals, AST_Equals

from .node_atoms import Void, AST_Void, VisitAtomic
from .node_atoms import Neg, AST_Neg
from .node_atoms import Complement, AST_Complement
from .node_atoms import New, AST_New, VisitNew
from .node_atoms import Id, AST_Id, VisitEqualAtomic
from .node_atoms import Int, AST_Int
from .node_atoms import Str, AST_Str
from .node_atoms import Bool, AST_Bool

class CoolSemanticChecking(VisitorBase):
    @visitor.add(node_type= AST_Program, accion_class= VisitProgram, result= Program)
    #class def 
    @visitor.add(node_type= AST_CoolClass, accion_class= VisitCoolClass, result= CoolClass)
    @visitor.add(node_type= AST_AtrDef, accion_class= VisitAttrDef, result= AtrDef)
    @visitor.add(node_type= AST_FuncDef, accion_class= VisitFuncDef, result= FuncDef)
    # expr dispatch
    @visitor.add(node_type= AST_CastingDispatch, accion_class= VisitCastingDispatch, result= CastingDispatch)
    @visitor.add(node_type= AST_Dispatch, accion_class= VisitDispatch, result= Dispatch)
    @visitor.add(node_type= AST_StaticDispatch, accion_class= VisitStaticDispatch, result= StaticDispatch)
    # expr statement
    @visitor.add(node_type= AST_Assing, accion_class= VisitAssing, result= Assing)
    @visitor.add(node_type= AST_IfThenElse, accion_class= VisitIfThenElse, result= IfThenElse)
    @visitor.add(node_type= AST_While, accion_class= VisitWhile, result= While)
    @visitor.add(node_type= AST_Block, accion_class= VisitBlock, result= Block)
    @visitor.add(node_type= AST_LetIn, accion_class= VisitLetIn, result= LetIn)
    @visitor.add(node_type= AST_Case, accion_class= VisitCase, result= Case)
    # expr binary
    @visitor.add(node_type= AST_Sum, accion_class= VisitBinary, result= Sum)
    @visitor.add(node_type= AST_Rest, accion_class= VisitBinary, result= Rest)
    @visitor.add(node_type= AST_Div, accion_class= VisitBinary, result= Div)
    @visitor.add(node_type= AST_Mult, accion_class= VisitBinary, result= Mult)
    @visitor.add(node_type= AST_Less, accion_class= VisitBinary, result= Less)
    @visitor.add(node_type= AST_LessOrEquals, accion_class= VisitBinary, result= LessOrEquals)
    @visitor.add(node_type= AST_Equals, accion_class= VisitBinary, result= Equals)
    # expr atomic
    @visitor.add(node_type= AST_New, accion_class= VisitNew, result= New)
    @visitor.add(node_type= AST_Neg, accion_class= VisitAtomic, result= Neg)
    @visitor.add(node_type= AST_Complement, accion_class= VisitAtomic, result= Complement)
    @visitor.add(node_type= AST_Void, accion_class= VisitAtomic, result= Void)
    @visitor.add(node_type= AST_Id, accion_class= VisitEqualAtomic, result= Id)
    @visitor.add(node_type= AST_Int, accion_class= VisitEqualAtomic, result= Int)
    @visitor.add(node_type= AST_Str, accion_class= VisitEqualAtomic, result= Str)
    @visitor.add(node_type= AST_Bool, accion_class= VisitEqualAtomic, result= Bool)

    def __init__(self, errors) -> None:
        super().__init__(errors)
    
    @visitor.on("node")
    def visit(node, scope):
        pass