from typing import List
from cool_cmp.shared.token import Token
from cool_cmp.shared.ast import BaseAST
from cool_cmp.shared.pipeline import IPipeable

class IParser(IPipeable):
    """
    Parser interface to implement
    """
    def __call__(self, tokens:List[Token]) -> BaseAST:
        raise NotImplementedError()
