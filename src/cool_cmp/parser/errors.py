"""
Parser errors
"""

from cool_cmp.shared.errors import CoolError
from cool_cmp.shared.token import ICoolToken

class SyntacticCoolError(CoolError):
    """
    Error class for syntactic errors
    """

    ERROR_TYPE = "SyntacticError"

    FORMAT = "({}, {}) - {}: {}"

    def __init__(self, error_message:str, error_token:ICoolToken):
        super().__init__(error_message)
        self.token = error_token

    def __str__(self):
        return self.FORMAT.format(self.token.get_position()[0],self.token.get_position()[1], self.ERROR_TYPE, f'ERROR at or near "{self.token.get_lex()}"')

