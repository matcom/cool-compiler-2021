import os
import dill
import sys
from typing import Any
from Lexer import CoolLexer
from Grammar import G
from cmp.parser_lr import LR1Parser

class Serializer:
    
    @staticmethod
    def save(target: Any, path: str) -> bool:
        try:
            with open(path, 'wb') as p:
                dill.dump(target, p)
            return True
        except:
            return False

    @staticmethod
    def load(path: str) -> Any:
        try:
            with open(path, 'rb') as p:
                return dill.load(p)
        except:
            return None

if __name__ == '__main__' :
    sys.setrecursionlimit(5000)
    lexer = CoolLexer()
    lexer.build()    
    Serializer.save(lexer, os.getcwd() + '/lexer')
    parser = LR1Parser(G)
    Serializer.save(parser, os.getcwd() + '/parser')