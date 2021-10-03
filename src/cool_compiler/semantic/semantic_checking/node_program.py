from .node__ import  Node
from ..tools import defVisitClass
from ..scope import Scope
from ..create_type import Program as  AST_Program

class Program(Node):
    def __init__(self, class_list) -> None:
        self.class_list = class_list

VisitProgram = defVisitClass(
    lambda self, node, error, scope = Scope() : self.gclss.visit_all(node.class_list, scope)
)