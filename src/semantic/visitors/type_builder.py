from utils.ast import *
from utils import visitor
from utils.errors import *
from semantic.types import *
from semantic.tools import Context

class TypeBuilder:
    def __init__(self):
        pass

    @visitor.on('node')
    def visit(self, node):
        pass

