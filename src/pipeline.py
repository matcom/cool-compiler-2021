from utils.semantic import Scope, Context
from visitors.Depicter import Depicter#, Formatter
from visitors.Collector import TypeCollector
from visitors.Builder import TypeBuilder
from visitors.Checker import TypeChecker
from visitors.Inferencer import Inferencer
from visitors.Executor import Executor, RuntimeException
from visitors.CooltoCil import COOLToCILVisitor
from visitors.CilDepicter import get_formatter



class Pipeline():
    def __init__(self, program, lexer, parser, verbose=False):
        self.context: Context = Context()
        self.errors = []
        self.scope: Scope = Scope()
        self.program = program
        self.lexer = lexer
        self.parser = parser
        
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
                    MIPSVisitor = CILToMIPSVisitor()
                    MIPSAst = MIPSVisitor.visit(cil_ast)
                    MIPSFormatter = MIPSAstFormatter()
                    mipsCode = MIPSFormatter.visit(MIPSAst)
                    self.mipsCode = mipsCode