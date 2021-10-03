from .node__ import Node
from ..__dependency import Type
from ..tools import VisitBase
from ..factory_return_ast import Program as AST_Program

class Program(Node):
    def __init__(self, class_list) -> None:
        self.class_list = class_list

class VisitProgram(VisitBase):
    def visit(self, node : AST_Program) : 
        for name, lineno, index in node.names_list:
            if name in self.gclss.global_types:
                self.gclss.cool_error(lineno, index)
                self.gclss.cool_error.add_semantic_error(f"{name} is already defined")
            else: self.gclss.global_types[name] = Type(name)

        class_list = self.visit_all(node.class_list)
        return class_list,
