from typing import List
class CoolError:
    """
    Base Cool Error
    """

    ERROR_TYPE = "CoolError"

    FORMAT = "{}: {}"

    def __init__(self, msg:str):
        self.error = msg
    
    def print_error(self):
        print(str(self))

    def __str__(self):
        return self.FORMAT.format(self.ERROR_TYPE, self.error)

    def __repr__(self):
        return str(self)

class IErrorTraceable:
    """
    Interface for error tracking system
    """

    def add_error(self, error:CoolError):
        raise NotImplementedError()

    def get_errors(self)->List[CoolError]:
        raise NotImplementedError()

class ErrorTracker(IErrorTraceable):
    """
    Basic Error tracking system
    """

    def __init__(self):
        self.__errors = []
    
    def add_error(self, error:CoolError):
        self.__errors.append(error)

    def get_errors(self)->List[CoolError]:
        return self.__errors