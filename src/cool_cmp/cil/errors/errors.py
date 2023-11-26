from error.errors import RunError

ZERO_DIVISION = "Divison by 0 not defined."

class AbortError(RunError):
    ERROR_TYPE = "AbortError"
    def __init__(self, type_name):
        self.typex = type_name

    def __str__(self):
        return f""
