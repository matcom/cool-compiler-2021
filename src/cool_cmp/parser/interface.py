from typing import List
from cool_cmp.shared.token import ICoolToken
from cool_cmp.shared.ast import BaseAST
from cool_cmp.shared import ICoolService

class IParser(ICoolService):
    """
    Parser interface to implement
    """

    def __call__(self, tokens:List[ICoolToken]) -> BaseAST:
        raise NotImplementedError()
