from cool_compiler.types.build_in_types import self


class CoolError:
    def __init__(self, code : str) -> None:
        self._list = []
        self.code = code
        self.pos = None
        self.text = None
    
    def any(self):
        if any(self._list):
            for msg in self._list:
                print(msg)
            return True
        return False   
                
    def __call__(self, lineno, index):
        self.pos = (lineno, self.find_column(index))
        return self

    def find_column(self, index):
        last_cr = self.code.rfind('\n', 0, index)
        if last_cr < 0:
            last_cr = 0
        column = (index - last_cr)
        return column if column != 0 else 1

    def __add(self, etype, text):
        self._list.append(f'{self.pos} - {etype}: {text}')

    def get_handler(self, lineno, index) -> self:
        l = lineno + 0
        i = index + 0
        return lambda : self.__call__(l,i)
        
    def add_lexical(self, text):
        self.__add("LexicographicError", text)
    
    def add_syntactic(self, text):
        self.__add("SyntacticError", text)

    def add_name_error(self, text):
        self.__add("NameError", text)
        
    def add_type_error(self, basee, ttype = ''):
        self.__add("TypeError", f'{basee}  {ttype}')

    def add_attribute_error(self, ttype, attr):
        self.__add("AttributeError", f'{attr} in {ttype} type')
        
    def add_semantic_error(self, text):
        self.__add("SemanticError", text)