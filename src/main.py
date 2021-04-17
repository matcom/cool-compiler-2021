from cool_cmp.lexer.interface import ILexer
from cool_cmp.lexer import LexerPipeline
from cool_cmp.parser.interface import IParser
from cool_cmp.parser import ParserPipeline
from cool_cmp.semantic.interface import ISemantic
from cool_cmp.semantic import SemanticPipeline
from cool_cmp.cil.interface import ICil
from cool_cmp.cil import CilPipeline
from cool_cmp.mips.interface import IMips
from cool_cmp.mips import MipsPipeline
from cool_cmp.shared.token import ICoolToken
from cool_cmp.shared.ast import BaseAST
from cool_cmp.shared.ast.cool import ClassDeclarationNode, ProgramNode
# from cool_cmp.lexer.lexer import PlyLexer
from cool_cmp.shared.errors import CoolError
from typing import List, Tuple

# Mock implementations

class MockLexer(ILexer):
    """
    Mock implementation of lexer
    """
    program = "class ` \n\tCoolClass\n{}"
    class MockToken(ICoolToken):
        def set_lex(self, lex:str):
            self.lex = lex

        def set_type(self, typex:str):
            self.typex = typex

        def set_position(self, line:int, column:int):
            self.line = line
            self.column = column

        def get_lex(self)->str:
            return self.lex

        def get_type(self)->str:
            return self.typex

        def get_position(self)->Tuple[int,int]:
            return (self.line, self.column)

    @property
    def mock_tokens(self)->List[ICoolToken]:
        info = [
            ("class", "CLASS", 0, 0),
            ("CoolClass", "ID", 1, 0),
            ("{", "OCUR", 2, 0),
            ("}", "CCUR", 2, 1),
        ]
        tokens = []
        for lex, typex, line, col in info:
            token = MockLexer.MockToken()
            token.set_lex(lex); token.set_type(typex); token.set_position(line, col)
            tokens.append(token)
        return tokens


    @property
    def name(self)->str:
        return "lexer"
    
    errors = []

    def add_error(self, error:CoolError):
        self.errors.append(error)
    
    def get_errors(self)->List[CoolError]:
        return self.errors

    def __call__(self, program_string:str) -> List[ICoolToken]:
        print("Tokenizing program:\n", program_string)
        return self.mock_tokens

class MockParser(IParser):
    """
    Mock implementation of parser
    """

    @property
    def name(self)->str:
        return "parser"

    def __call__(self, tokens:List[ICoolToken]) -> BaseAST:
        print("Building AST from tokens",tokens)
        class_token = MockLexer().mock_tokens
        class_token = class_token[0]
        return BaseAST(ProgramNode([ClassDeclarationNode(class_token.lex, [], None, class_token.line, class_token.column)]))

    errors = []

    def add_error(self, error:CoolError):
        self.errors.append(error)
    
    def get_errors(self)->List[CoolError]:
        return self.errors

class MockSemantic1(ISemantic):
    """
    Mock Semantic interface 1
    """

    @property
    def name(self)->str:
        return "semantic1"

    def __call__(self, ast:BaseAST) -> BaseAST:
        print("Doing some crazy shit with ast, apply visitor, etc")
        print("Collecting Types...")
        print("Building Types...")
        print("Type Checking...")
        print("Setted mock1 property to true as a way of communicate between pipes")
        ast.mock1 = True
        return ast
    
    errors = []

    def add_error(self, error:CoolError):
        self.errors.append(error)
    
    def get_errors(self)->List[CoolError]:
        return self.errors

class MockSemantic2(ISemantic):
    """
    Mock Semantic interface 2
    """

    @property
    def name(self)->str:
        return "semantic2"

    def __call__(self, ast:BaseAST) -> BaseAST:
        print("Doing another crazy shit with previously returned ast")
        print("Verifying that ast has mock1 property", hasattr(ast, "mock1"))
        print("Converting COOL AST into CIL AST...")
        return ast
    
    errors = []

    def add_error(self, error:CoolError):
        self.errors.append(error)
    
    def get_errors(self)->List[CoolError]:
        return self.errors

class MockCil1(ICil):
    """
    Mock Cil interface 1
    """

    @property
    def name(self)->str:
        return "cil1"

    def __call__(self, ast:BaseAST) -> BaseAST:
        print("Optimizing CIL AST...")
        return ast

    errors = []

    def add_error(self, error:CoolError):
        self.errors.append(error)
    
    def get_errors(self)->List[CoolError]:
        return self.errors

class MockCil2(ICil):
    """
    Mock Cil interface 2
    """

    @property
    def name(self)->str:
        print("Converting CIL AST into MIPS AST...")
        return "cil2"

    def __call__(self, ast:BaseAST) -> BaseAST:
        return ast

    errors = []

    def add_error(self, error:CoolError):
        self.errors.append(error)
    
    def get_errors(self)->List[CoolError]:
        return self.errors

class MockMips1(IMips):
    """
    Mock MIPS interface 1
    """

    @property
    def name(self)->str:
        return "mips1"

    def __call__(self, ast:BaseAST) -> BaseAST:
        print("Doing MIPS things...")
        return ast

    errors = []

    def add_error(self, error:CoolError):
        self.errors.append(error)
    
    def get_errors(self)->List[CoolError]:
        return self.errors

class MockMips2(IMips):
    """
    Mock MIPS interface 2
    """

    @property
    def name(self)->str:
        return "mips2"

    def __call__(self, ast:BaseAST) -> BaseAST:
        print("Generating MIPS code...")
        return ast

    errors = []

    def add_error(self, error:CoolError):
        self.errors.append(error)
    
    def get_errors(self)->List[CoolError]:
        return self.errors

# Testing pipeline

# pipe = LexerPipeline(MockLexer())

# # pipe = LexerPipeline(PlyLexer())

# pipe = ParserPipeline(pipe, MockParser())

# pipe = SemanticPipeline(pipe, MockSemantic1(), MockSemantic2())

# pipe = CilPipeline(pipe, MockCil1(), MockCil2())

# pipe = MipsPipeline(pipe, MockMips1(), MockMips2())

# result = pipe(MockLexer.program)

# print(result.get_errors())

# from cool2.main import main 

# main('src/a.cl', None,False,False,False,False,False)

if __name__ == "__main__":
    import sys
    with open(sys.argv[1]) as file:
        program = file.read()
        pipe = LexerPipeline()
        result = pipe(program)
        for err in result.get_errors():
            if isinstance(err, str):
                print(err)
            else:
                err.print_error()
        if result.get_errors():
            exit(1)
    with open(sys.argv[2], 'w') as file:
        file.write("GENERATED MIPS")
    
    exit(0)
