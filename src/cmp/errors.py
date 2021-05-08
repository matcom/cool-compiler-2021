class LexicographicError:
    @staticmethod
    def text(line, column, text):
        return  '(%s, %s) - LexicographicError: %s'%(line, column, text)

class SyntacticError:
    @staticmethod
    def text(line, column, text):
        return  '(%s, %s) - SyntacticError: ERROR at or near "%s"'%(line, column, text)
    @staticmethod
    def text_eof():
        return '(0, 0) - SyntacticError: ERROR at or near "EOF"'

class SemanticError(Exception):
    @property
    def text(self):
        return self.args[0]
    
    @staticmethod
    def set_error(line, column, text):
        return  '(%s, %s) - SemanticError: %s'%(line, column, text)

class TypesError(Exception):
    @property
    def text(self):
        return self.args[0]
    
    @staticmethod
    def set_error(line, column, text):
        return  '(%s, %s) - TypeError: %s'%(line, column, text)

class NamesError(Exception):
    @property
    def text(self):
        return self.args[0]
    
    @staticmethod
    def set_error(line, column, text):
        return  '(%s, %s) - NameError: %s'%(line, column, text)

class AttributesError(Exception):
    @property
    def text(self):
        return self.args[0]
    
    @staticmethod
    def set_error(line, column, text):
        return  '(%s, %s) - AttributeError: %s'%(line, column, text)

class ParamError(Exception):
    @property
    def text(self):
        return self.args[0]
    
    @staticmethod
    def set_error(line, column, text):
        return  '(%s, %s) - SemanticError: %s'%(line, column, text)