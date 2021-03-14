"""
AST package
"""

from cool_cmp.shared.errors import ErrorTracker

class Node:
    """
    Base node for AST
    """
    def __init__(self,row:int=None,column:int=None):
        self.row = row
        self.column = column

class BaseAST(ErrorTracker):
    """
    Base AST class
    """

    def __init__(self, initial_node:Node):
        self.node = initial_node
        super().__init__()
