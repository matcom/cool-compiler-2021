from cool_cmp.shared.ast import BaseAST
from cool_cmp.shared.pipeline import IPipeable

class ISemantic(IPipeable):
    """
    Semantic interface to implement
    """

    @property
    def name(self)->str:
        raise NotImplementedError()

    def __call__(self, ast:BaseAST) -> BaseAST:
        raise NotImplementedError()

