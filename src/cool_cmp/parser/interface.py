from typing import List
from cool_cmp.shared.token import ICoolToken
from cool_cmp.shared.ast import BaseAST
from cool_cmp.shared import ICoolService
from cool2.cmp.pycompiler import AttributeProduction

class IParser(ICoolService):
    """
    Parser interface to implement
    """

    def __call__(self, tokens:List[ICoolToken], context) -> List[AttributeProduction]:
        raise NotImplementedError()
