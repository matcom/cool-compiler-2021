from cool_cmp.shared.ast import BaseAST
from cool_cmp.shared import ICoolService

class ISemantic(ICoolService):
    """
    Semantic interface to implement
    """

    def __call__(self, ast:BaseAST) -> BaseAST:
        raise NotImplementedError()

