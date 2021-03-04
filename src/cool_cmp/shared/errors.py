class CoolError:
    """
    Base Cool Error
    """

    def __init__(self, msg:str):
        self.error = msg
    
    def print_error(self):
        print(self.error)

class ErrorTracker:

    def __init__(self):
        self.errors = []
    
    def add_error(self, error:CoolError):
        self.errors.append(error)