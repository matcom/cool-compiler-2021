from typing import List
from cool2.cool.error.errors import CoolError

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