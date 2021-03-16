from utils.ast import *
from utils import visitor
from utils.errors import *
from semantic.types import *
from semantic.tools import Context

class TypeBuilder:
    def __init__(self, context : Context, errors : list) -> None:
        self.context:Context = context
        self.errors:list = errors
        self.current_type:Type = None

    @visitor.on('node')
    def visit(self, node):
        pass

