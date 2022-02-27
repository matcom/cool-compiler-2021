from utils.semantic import Scope, Context
from visitors.Depicter import Depicter#, Formatter
from visitors.Collector import TypeCollector
from visitors.Builder import TypeBuilder
from visitors.Checker import TypeChecker
from visitors.Inferencer import Inferencer
from visitors.Executor import Executor, RuntimeException
# from visitors.CooltoCil import COOLToCILVisitor
from visitors.CooltoCilM import COOLToCILVisitor
from visitors.CilDepicter import get_formatter
# from visitors.CiltoMips import CiltoMipsVisitor

from cil_ast.cil_ast import get_formatter
from mmips.CilToMipsVisitor import CILToMIPSVisitor
from mmips.MIPSAstFormatter import MIPSAstFormatter

# from visitors.Cil2MipsCurrent import CILToMipsVisitor

class Pipeline():
    def __init__(self, program, lexer, parser, verbose=False):
        self.context: Context = Context()
        self.errors = []
        self.scope: Scope = Scope()
        self.program = program
        self.lexer = lexer
        self.parser = parser
        
        # current_position = 0
        # for char in self.program:

        # self.tokens = self.lexer.lexer(self.program)
        
        # self.tokens = [ token for token in self.tokens if token.token_type not in ['space', 'newLine', 'chunkComment', 'lineComment', 'tab']]

        # derivations, operations = self.parser.Parser(self.tokens, True)

        self.ast = self.parser.parse(lexer, program)#= evaluate_reverse_parse(derivations, operations, self.tokens)
        self.errors = self.lexer.errors + self.parser.errors
        if len(self.errors) != 0:
            return
        
        if self.ast is None:
            return
                
        self.depicter = Depicter()
        if verbose:
            print(self.depicter.visit(self.ast,0), '\n')
            print()
        
        self.typeCollector = TypeCollector(self.context, self.errors)
        self.typeCollector.visit(self.ast)
        if len(self.errors) == 0:
            self.typeBuilder = TypeBuilder(self.context, self.errors)
            self.typeBuilder.visit(self.ast)
            scope = Scope()
            if len(self.errors) == 0:
                self.typeChecker = TypeChecker(self.context, self.errors)
                self.typeChecker.visit( self.ast, scope)
                if len(self.errors) == 0:
                    self.coolToCil = COOLToCILVisitor(self.context)
                    cil_ast = self.coolToCil.visit(self.ast, scope)
                    __a = 0
                    # print(get_formatter(cil_ast))
                    # self.cilToMips = CiltoMipsVisitor(self.context)
                    # self.cilToMips.visit(cil_ast)
                    # with open('out', 'w') as f:
                    #     mips_code = self.cilToMips.data + self.cilToMips.code
                    #     for line in mips_code:
                    #         f.write(line+'\n')
                    MIPSVisitor = CILToMIPSVisitor()
                    MIPSAst = MIPSVisitor.visit(cil_ast)
                    MIPSFormatter = MIPSAstFormatter()
                    mipsCode = MIPSFormatter.visit(MIPSAst)
                    # MIPSVisitor = CILToMipsVisitor()
                    # mipsCode = MIPSVisitor.visit(cil_ast)
                    self.mipsCode = mipsCode
                    # with open('asd.mips', 'w') as f:
                    #     f.write(mipsCode)
                    #     f.close()

        if verbose:
            print('This is after infering types:')
            print()
            print(self.depicter.visit(self.ast,0))
            print()
        # self.executor = Executor(self.context)
        
        # if len(self.errors) == 0:
        #     try:
        #         executorScope = Scope()
        #         self.executor.visit(self.ast,executorScope)
        #         print()
        #         print('Done!!')
        #     except RuntimeException as e:
        #         print(e)
        #         print()
        # for error in self.errors:
        #     print(error)