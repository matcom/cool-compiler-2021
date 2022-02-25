class Token:
    def __init__(self, name, value, line, lexpos):
        self.name = name
        self.value = value
        self.line = line
        self.lexpos = lexpos