class SyntacticError:
   def __init__(self, token, line, col) -> None:
      self.line = line
      self.token = token
      self.col = col

   def __str__(self) -> str:
       return f'({self.line}, {self.col}) - \
       SyntacticError: ERROR at or near "{self.token}"'
