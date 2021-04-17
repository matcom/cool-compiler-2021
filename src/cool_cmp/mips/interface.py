
from cool_cmp.shared.ast import BaseAST
from cool_cmp.shared import ICoolService

class IMips(ICoolService):
    """
    MIPS interface to implement
    """
    
    def __call__(self, ast:BaseAST) -> BaseAST:
        raise NotImplementedError()

