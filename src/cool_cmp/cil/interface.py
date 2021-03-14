from cool_cmp.shared.ast import BaseAST
from cool_cmp.shared import ICoolService

class ICil(ICoolService):
    """
    CIL interface to implement
    """

    def __call__(self, ast:BaseAST) -> BaseAST:
        raise NotImplementedError()
