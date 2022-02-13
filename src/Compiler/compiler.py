from Semantic.Semantic import COOL_Semantic_Checker
from Parser.Parser import COOL_Parser
from Semantic.scope import COOL_Scope
from Lexer.Lexer import COOL_Lexer
import sys

class COOL_Compiler:

    def __init__(self):
        self.cool_lexer = COOL_Lexer()
        self.cool_parser = COOL_Parser(self.cool_lexer)
    
    def run(self, code):
        # Lexic & Sintactic Analizer
        ast = self.cool_parser.run(code)
        
        if self.cool_lexer.errors:
            exit(1)

        if self.cool_parser.errors:
            for error in self.cool_parser.error_list:
                sys.stdout.write(f'{error}\n')
            exit(1)
        
        # Semantic Analyzer
        cool_checker = COOL_Semantic_Checker()
        scope = cool_checker.visit(ast)
        
        if cool_checker.errors:
            exit(1)


def main(file):
    with open(file, "r") as fd:
        data = fd.read()
    data = data.replace('\t', "    ")

    _cmp = COOL_Compiler()
    _cmp.run(data)

if __name__ == '__main__':
    main(sys.argv[1])
