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
from cool_cmp.shared.token import Token
from cool_cmp.shared.ast import BaseAST
from cool_cmp.shared.ast.cool import ClassDeclarationNode, ProgramNode
from typing import List

# Mock implementations

class MockLexer(ILexer):
    """
    Mock implementation of lexer
    """
    program = "class \nCoolClass\n{}"
    mock_tokens = [
            Token("class",0,0),
            Token("CoolClass",1,0),
            Token("{",2,0),
            Token("}",2,1)
        ]

    @property
    def name(self)->str:
        return "lexer"


    def __call__(self, program_string:str) -> List[Token]:
        print("Tokenizing program:\n", program_string)
        return self.mock_tokens

class MockParser(IParser):
    """
    Mock implementation of parser
    """

    @property
    def name(self)->str:
        return "parser"

    def __call__(self, tokens:List[Token]) -> BaseAST:
        print("Building AST from tokens",tokens)
        class_token = MockLexer.mock_tokens[0]
        return BaseAST(ProgramNode([ClassDeclarationNode(class_token.lex, [], None, class_token.line, class_token.column)]))

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


# Testing pipeline

pipe = LexerPipeline(MockLexer())

pipe = ParserPipeline(pipe, MockParser())

pipe = SemanticPipeline(pipe, MockSemantic1(), MockSemantic2())

pipe = CilPipeline(pipe, MockCil1(), MockCil2())

pipe = MipsPipeline(pipe, MockMips1(), MockMips2())

# print(pipe(MockLexer.program))

from cool2.main import main 

main('src/a.cl', None,False,False,False,False,False)