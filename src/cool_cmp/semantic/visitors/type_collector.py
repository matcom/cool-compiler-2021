import cool_cmp.shared.visitor as visitor
from cool_cmp.semantic.interface import  IContext
from cool_cmp.shared.errors import ErrorTracker
from cool_cmp.shared.ast.cool import *

class TypeCollectorVisitor:
    """
    Collects the types by saving them in a Context
    """
    
    def __init__(self, error_tracker:ErrorTracker, context:IContext=None):
        self.errors = error_tracker
        self.context = context
    
    @visitor.on('node')
    def visit(self, node):
        pass
    
    @visitor.when(ProgramNode)
    def visit(self, node:ProgramNode):
        pass # TODO
            
    

