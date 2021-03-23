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

    def find_column(self, index):
        last_cr = self.code.rfind('\n', 0, index)
        if last_cr < 0:
            last_cr = 0
        column = (index - last_cr)
        return column

    def __add(self, etype, text):
        self._list.append(f'{self.pos} - {etype}: {text}')

    def add_lexical(self, text):
        self.__add("LexicographicError", text)
