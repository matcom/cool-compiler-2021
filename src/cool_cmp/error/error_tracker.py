from typing import List
from error.errors import CoolError, PositionError

class LexerCoolError(PositionError):
    """
    Error class for lexical errors
    """
    
    FORMAT = "({}, {}) - {}: {}"
    
    ERROR_TYPE = "LexicographicError"

class ErrorTracker():
    """
    Basic Error tracking system
    """

    def __init__(self):
        self.__errors = []
    
    def add_error(self, error:CoolError):
        self.__errors.append(error)

    def get_errors(self)->List[CoolError]:
        return self.__errors