
class CoolError(Exception):
    """
    Base Cool Error
    """
    
    @property
    def text(self):
        return str(self)

    ERROR_TYPE = "CoolError"

    FORMAT = "{}: {}"

    def __init__(self, msg:str, *args):
        self.error = msg
        self.args = args
    
    def print_error(self):
        print(str(self))

    def __str__(self):
        return CoolError.FORMAT.format(self.ERROR_TYPE, self.error.format(*self.args))

    def __repr__(self):
        return str(self)

class PositionError(CoolError):
    """
    Error class for positional errors
    """
    
    FORMAT = "({}, {}) - {}: ERROR {}"

    def __init__(self, error_message:str, *args, **kwargs):
        """
        kwargs:  
        token: The token where the error is  
        row: Row error  
        column: Column error  
        lex: Representation of the error  
        """
        super().__init__(error_message, *args)
        self.__row = kwargs.get("row")
        self.__column = kwargs.get("column")
        self.lex = kwargs.get("lex")
        if "token" in kwargs:
            self.__row = kwargs["token"].lex[1]
            self.__column = kwargs["token"].lex[2]
            self.lex = kwargs["token"].lex[0]
            self.token = kwargs["token"]
        else:
            self.token = None

    @property
    def row(self):
        return self.__row if self.token == None else self.token.line
    
    @property
    def column(self):
        return self.__column if self.token == None else self.token.column 

    def set_position(self, row:int, column:int):
        self.__row = row
        self.__column = column

    def __str__(self):
        if self.row == None or self.column == None:
            return super().__str__()
        return self.FORMAT.format(self.row,self.column, self.ERROR_TYPE, self.error.format(*self.args))

class RunError(CoolError):
    ERROR_TYPE = "RunError"
