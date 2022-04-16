from pathlib import Path
from utils.errors import *
from utils.utils import Utils
from lexing.lexer import Lexer
from parsing.parser import Parser
from semantic.semantic import SemanticAnalyzer
from code_generation.code_generation import CodeGeneration

class Compiler:

    def __init__(self, input_file:str, output_file:str, debug:bool):
        '''
        Inicializa las variables a utilizar y 
        ejecuta el pipeline del proyecto.
        '''
        self.input_file = Path(input_file)
        self.output_file = Path(output_file)
        self.debug = debug
        self.code = ''
        self.lexer = None
        self.parser = None
        self.ast = None
        self.context = None
        self.scope = None

        name = Utils.GetName(input_file)
        self.debug_path = f'./debug/{name}'

        if not str(self.input_file).endswith('.cl'):
            error_text = CompilerError.WRONG_EXTENTION
            print(CompilerError(0, 0, error_text))
            exit(1)

        try:
            with open(self.input_file, encoding='utf-8') as file:
                self.code += file.read()
        except (IOError, FileNotFoundError):
            error_text = CompilerError.UNKNOWN_FILE % str(self.input_file)
            print(CompilerError(0, 0, error_text))
            exit(1)

        Utils.Write(self.debug_path, '.cl', self.code) if self.debug else None
        self.steps = [ self.lexing, self.parsing, self.semantics, self.code_generation ]

    def compile(self):
        '''
        Ejecuta el pipeline para correr cada fase.
        '''
        for step in self.steps:
            step()

    def lexing(self):
        '''
        Lleva a cabo el análisis lexicográfico.
        '''
        self.lexer = Lexer()
        tokens = self.lexer.tokenizer(self.code)
        Utils.Write(self.debug_path, '.lexer', '\n'.join(repr(token) 
                                for token in tokens)) if self.debug else None

        # for token in tokens:
        #     print(token)

        if len(self.lexer.errors) > 0:
            print(self.lexer.errors[0])
            exit(1)
        elif len(tokens) == 0:
            error_text = SyntacticError.ERROR % 'EOF'
            print(SyntacticError(0, 0, error_text))
            exit(1)
        # else:
        #     print('COMPLETED LEXER!!!')

    def parsing(self):
        '''
        Lleva a cabo el análisis sintáctico.
        '''
        self.parser = Parser(lexer=self.lexer)
        self.ast = self.parser(self.code)
        Utils.Write(self.debug_path, '.parser', '\n'.join(repr(rule) 
                for rule in Utils.GetRulesParsing())) if self.debug else None

        if len(self.parser.errors) > 0:
            print(self.parser.errors[0])
            exit(1)
        # else:
        #     print('COMPLETED PARSING!!!')

    def semantics(self):
        '''
        Lleva a cabo el análisis semántico.
        '''
        semantic_analyzer = SemanticAnalyzer(self.ast, 
                                        self.debug_path, debug=self.debug)
        self.ast, self.context, self.scope = semantic_analyzer.analyze()

        if len(semantic_analyzer.errors) > 0:
            print(semantic_analyzer.errors[0])
            exit(1)
        # else:
        #     print('COMPLETED SEMANTIC ANALYSER!!!')

    def code_generation(self):
        '''
        Lleva a cabo la generación de código.
        '''
        code_generation = CodeGeneration(self.ast, self.context, self.scope, self.debug_path)
        self.mips_code = code_generation.code_generation()
        self.output_file.write_text(self.mips_code)

        # print('COMPLETED CODE GENERATION!!!')


def main():

    args = Utils.GetArguments()

    input_file = args.input_file
    output_file = args.output_file
    debug = args.debug

    Compiler(input_file, output_file, debug).compile()

if __name__ == '__main__':
    main()
